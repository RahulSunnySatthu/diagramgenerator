interface Props {
    src: string;
}

export default function DiagramViewer({ src }: Props) {
    return (
        <div className="mt-6 max-w-3xl mx-auto bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Generated Diagram:</h2>
            <img src={src} alt="Generated diagram" className="w-full" />
        </div>
    );
}
