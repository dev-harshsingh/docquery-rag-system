import { useState } from "react";
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Stack,
  CircularProgress,
} from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {
    if (!file) return alert("Select a file first");

    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    alert("File uploaded. Ingestion started.");
  };

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    const res = await fetch("http://localhost:5000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    setAnswer(data.answer);
    setSources(data.sources || []);
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 6 }}>
      <Typography variant="h3" align="center" gutterBottom>
        📄 DocQuery AI
      </Typography>

      <Typography align="center" color="text.secondary" mb={4}>
        Ask questions directly from your documents
      </Typography>

      <Stack spacing={3}>
        {/* Upload Card */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Upload Document
            </Typography>

            <TextField
              type="file"
              fullWidth
              onChange={(e) => setFile(e.target.files[0])}
            />

            <Button
              variant="contained"
              startIcon={<UploadFileIcon />}
              sx={{ mt: 2 }}
              onClick={uploadFile}
            >
              Upload & Process
            </Button>
          </CardContent>
        </Card>

        {/* Query Card */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Ask a Question
            </Typography>

            <TextField
              fullWidth
              placeholder="What is this document about?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <Button
              variant="contained"
              startIcon={<QuestionAnswerIcon />}
              sx={{ mt: 2 }}
              onClick={askQuestion}
            >
              Ask
            </Button>
          </CardContent>
        </Card>

        {/* Loading */}
        {loading && (
          <Stack alignItems="center">
            <CircularProgress />
            <Typography mt={1} color="text.secondary">
              Thinking...
            </Typography>
          </Stack>
        )}

        {/* Answer */}
        {answer && (
          <Card sx={{ borderLeft: "4px solid #6366f1" }}>
            <CardContent>
              <Typography variant="h6">Answer</Typography>
              <Typography mt={1}>{answer}</Typography>

              <Typography mt={3} variant="subtitle1">
                Sources
              </Typography>

              {sources.map((s, i) => (
                <Typography key={i} variant="body2" color="text.secondary">
                  • {s.source} (page {s.page})
                </Typography>
              ))}
            </CardContent>
          </Card>
        )}
      </Stack>
    </Container>
  );
}

export default App;
