import express from "express";
import cors from "cors";
import multer from "multer";
import { createClient } from "redis";
import path from "path";
import fs from "fs";
import axios from "axios";

const PYTHON_AI_SERVICE_URL = "http://localhost:8000";


const app = express();
app.use(cors());
app.use(express.json());

const redisClient = createClient({
  socket: {
    host: "127.0.0.1",
    port: 6379,
  },
});


redisClient.connect();

redisClient.on("connect", () => {
  console.log("🟢 Connected to Redis");
});

redisClient.on("error", (err) => {
  console.error("🔴 Redis error:", err);
});


const uploadDir = path.join(process.cwd(), "uploads");

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const storage = multer.diskStorage({
  destination: uploadDir,
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({ storage });


app.get("/", (req, res) => {
  res.send("DOC-Query-SYS");
});

//UPLOAD DOCS
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = req.file.path;
    console.log("📁 File saved:", filePath);

    if (!redisClient.isReady) {
      return res.status(503).json({ error: "Redis not available" });
    }

    // ✅ PUSH JOB TO REDIS
    await redisClient.lPush(
      "ingest_queue",
      JSON.stringify({ file_path: filePath })
    );

    console.log("📤 Job pushed to Redis:", filePath);

    return res.status(202).json({
      message: "File uploaded successfully. Ingestion started.",
      file_path: filePath,
    });
  } catch (err) {
    console.error("🔥 Upload error:", err);
    return res.status(500).json({ error: "Upload failed" });
  }
});

//Query

app.post("/query", async (req, res) => {
  try {
    const { question } = req.body;

    if (!question) {
      return res.status(400).json({ error: "Question is required" });
    }

    // Forward request to Python AI service
    const response = await axios.post(
      `${PYTHON_AI_SERVICE_URL}/query`,
      { question },
      { timeout: 60_000 } 
    );

    return res.json(response.data);

  } catch (err) {
    console.error("🔥 Query error:", err.message);

    return res.status(500).json({
      error: "Failed to process query",
      details: err.message,
    });
  }
});


const PORT = 5000;
app.listen(PORT, () => {
  console.log(`🚀 Node server running on port ${PORT}`);
});
