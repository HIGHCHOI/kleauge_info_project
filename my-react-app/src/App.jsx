// src/App.jsx
import { useState } from "react";

function App() {
  const [userName, setUserName] = useState("");
  const [position, setPosition] = useState("중앙 미드필더");
  const [style, setStyle] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const handleRecommend = async () => {
    // (1) 요청 바디 만들기
    const bodyData = {
      position: position,
      style: style
    };

    try {
      // (2) FastAPI 서버 POST 요청
      const response = await fetch("http://127.0.0.1:8000/recommend?top_n=3", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData)
      });

      // (3) JSON 응답 파싱
      const data = await response.json();

      // data.recommendations = [ [teamName, score], ... ]
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error("추천 요청 실패:", error);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20, fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 24, marginBottom: 16 }}>K-League 팀 추천</h1>

      <div style={{ marginBottom: 12 }}>
        <label style={{ display: "block", marginBottom: 4 }}>이름 (선택):</label>
        <input
          type="text"
          value={userName}
          onChange={e => setUserName(e.target.value)}
          placeholder="홍길동"
          style={{
            width: "100%",
            padding: 8,
            border: "1px solid #ccc",
            borderRadius: 4
          }}
        />
      </div>

      <div style={{ marginBottom: 12 }}>
        <label style={{ display: "block", marginBottom: 4 }}>포지션:</label>
        <select
          value={position}
          onChange={e => setPosition(e.target.value)}
          style={{ padding: 8, border: "1px solid #ccc", borderRadius: 4 }}
        >
          <option value="중앙 미드필더">중앙 미드필더</option>
          <option value="수비수">수비수</option>
          <option value="공격수">공격수</option>
          <option value="골키퍼">골키퍼</option>
        </select>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label style={{ display: "block", marginBottom: 4 }}>스타일:</label>
        <textarea
          rows={3}
          value={style}
          onChange={e => setStyle(e.target.value)}
          placeholder="전방 압박, 점유율 기반, 빌드업 등"
          style={{
            width: "100%",
            padding: 8,
            border: "1px solid #ccc",
            borderRadius: 4
          }}
        />
      </div>

      <button
        onClick={handleRecommend}
        style={{
          padding: "8px 16px",
          backgroundColor: "#1976d2",
          color: "#fff",
          border: "none",
          borderRadius: 4,
          cursor: "pointer"
        }}
      >
        팀 추천 받기
      </button>

      <div style={{ marginTop: 20 }}>
        <h2 style={{ fontSize: 20 }}>추천 결과</h2>
        {recommendations.length > 0 ? (
          recommendations.map((item, idx) => (
           <div key={idx} style={{ padding: 10, marginBottom: 12, border: "1px solid #ccc", borderRadius: 6 }}>
            <h3>{idx + 1}위: {item.team_name}</h3>
            <p><strong>감독:</strong> {item.manager}</p>
            <p><strong>스타일:</strong> {item.team_style}</p>
            <p><strong>유사도 점수:</strong> {item.score}</p>
          </div>
          ))
        ) : (
          <p>아직 추천 결과가 없습니다.</p>
        )}
      </div>

    </div>
  );
}

export default App;

