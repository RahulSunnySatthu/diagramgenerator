import { useState } from 'react';
import QuestionForm from './components/QuestionForm';
import DiagramViewer from './components/DiagramViewer';

export default function App() {
  const [diagramSrc, setDiagramSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateDiagram = async (topic: string) => {
    setLoading(true);
    setError(null);
    setDiagramSrc(null);

    try {
      console.log("Sending request to backend with topic:", topic);

      const res = await fetch('https://your-backend-url.onrender.com/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();

      if (!res.ok || !data.diagram) {
        throw new Error(data.error || 'Invalid response from server');
      }

      console.log('Blockdiag code from server:', data.diagram);

      const svgUrl = await buildKrokiUrl(data.diagram);
      console.log('Kroki URL:', svgUrl);

      setDiagramSrc(svgUrl);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6 text-center">Visualize AI</h1>
      <QuestionForm onSubmit={handleGenerateDiagram} loading={loading} />
      {error && <p className="text-red-600 text-center mt-4">{error}</p>}
      {diagramSrc && <DiagramViewer src={diagramSrc} />}
    </div>
  );
}

async function buildKrokiUrl(diagramCode: string): Promise<string> {
  const compressed = await compressText(diagramCode);
  const encoded = toBase64Url(compressed);
  return `https://kroki.io/blockdiag/svg/${encoded}`;
}

async function compressText(text: string): Promise<Uint8Array> {
  const stream = new CompressionStream('deflate');
  const writer = stream.writable.getWriter();
  writer.write(new TextEncoder().encode(text));
  writer.close();

  const compressed = await new Response(stream.readable).arrayBuffer();
  return new Uint8Array(compressed);
}

function toBase64Url(bytes: Uint8Array): string {
  const binary = String.fromCharCode(...bytes);
  const base64 = btoa(binary);
  return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
