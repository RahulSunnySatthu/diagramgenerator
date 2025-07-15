import { useState } from 'react';

interface Props {
    onSubmit: (topic: string) => void;
    loading: boolean;
}

export default function QuestionForm({ onSubmit, loading }: Props) {
    const [topic, setTopic] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (topic.trim()) {
            onSubmit(topic.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-xl mx-auto bg-white p-4 rounded shadow">
            <textarea
                className="w-full border p-2 rounded resize-none"
                rows={4}
                placeholder="Enter your programming question or topic..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                disabled={loading}
            />
            <button
                type="submit"
                className="mt-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                disabled={loading}
            >
                {loading ? 'Generating...' : 'Generate Diagram'}
            </button>
        </form>
    );
}
