import { useState, useEffect } from "react";

function App() {
  const [deployments, setDeployments] = useState([]);
  const [selectedIssue, setSelectedIssue] = useState(null);

  const fetchDeployments = async () => {
    const url = selectedIssue ? `http://localhost:8000/api/deployments?parent_issue_number=${selectedIssue}`
                              : "http://localhost:8000/api/deployments";
    const res = await fetch(url);
    const data = await res.json();
    setDeployments(data);
  };

  const redeploy = async (user_request, parent_issue_number=null) => {
    const res = await fetch("http://localhost:8000/api/deployments/redeploy", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({user_request, parent_issue_number})
    });
    const data = await res.json();
    alert(`Redeployed! URL: ${data.url} | QA: ${data.qa_result}`);
    fetchDeployments();
  };

  useEffect(() => {
    fetchDeployments();
    const interval = setInterval(fetchDeployments, 5000); // 5초마다 상태 갱신
    return () => clearInterval(interval);
  }, [selectedIssue]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Real-time Deployment Dashboard</h1>
      <div className="mb-4">
        <input type="number" placeholder="Filter by Issue Number"
               onChange={e => setSelectedIssue(e.target.value)} />
        <button className="ml-2 px-2 py-1 bg-blue-500 text-white" onClick={fetchDeployments}>Filter</button>
      </div>
      <table className="w-full border">
        <thead>
          <tr>
            <th className="border px-2 py-1">ID</th>
            <th className="border px-2 py-1">Project</th>
            <th className="border px-2 py-1">URL</th>
            <th className="border px-2 py-1">QA</th>
            <th className="border px-2 py-1">Status</th>
            <th className="border px-2 py-1">Parent Issue</th>
            <th className="border px-2 py-1">Actions</th>
          </tr>
        </thead>
        <tbody>
          {deployments.map(d => (
            <tr key={d[0]}>
              <td className="border px-2 py-1">{d[0]}</td>
              <td className="border px-2 py-1">{d[3]}</td>
              <td className="border px-2 py-1"><a href={d[4]} target="_blank">{d[4]}</a></td>
              <td className="border px-2 py-1">{d[5]}</td>
              <td className={`border px-2 py-1 ${d[6]==="success"?"text-green-600":d[6]==="deploying"?"text-blue-600":"text-red-600"}`}>{d[6]}</td>
              <td className="border px-2 py-1">{d[2]}</td>
              <td className="border px-2 py-1 space-x-2">
                <button className="bg-green-500 text-white px-2 py-1"
                        onClick={() => redeploy("Re-deploy: " + d[3], d[1])}>
                  Deploy Again
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
