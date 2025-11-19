// API 래퍼 객체: 프론트엔드에서 백엔드 API를 호출할 때 사용합니다.
export const API = {

    // generateSite: 생성 요청을 보냅니다.
    // 입력: { prompt }  => 사용자가 입력한 설명 문자열
    // 반환: 백엔드가 반환한 JSON 응답
    generateSite: async ({ prompt }) => {
        // Vite 환경변수 `VITE_API_URL`이 설정되어 있으면 사용, 없으면 로컬 기본값 사용
        const base = import.meta.env.VITE_API_URL || "http://localhost:8000";

        // fetch로 POST 요청을 보냄
        const response = await fetch(`${base}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        // JSON 디코드 후 반환
        return response.json();
    },

    // deploySite: 배포 요청을 보냅니다.
    // 입력/반환 형태는 백엔드 /deploy 엔드포인트에 맞춰 사용합니다.
    deploySite: async ({ prompt }) => {
        const base = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const response = await fetch(`${base}/deploy`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });
        return response.json();
    },

};
