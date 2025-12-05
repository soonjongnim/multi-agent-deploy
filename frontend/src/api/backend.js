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

    // audio 파일 업로드 후 전사 결과를 반환합니다.
    // FormData에 'file' 키로 파일을 전달해야 합니다.
    uploadAudio: async (file) => {
        const base = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const fd = new FormData();
        fd.append('file', file, file.name);

        try {
            const response = await fetch(`${base}/transcribe`, {
                method: 'POST',
                body: fd,
            });

            // 네트워크 레벨에서 실패하면 above에서 throw, 여기는 정상적으로 응답받았을 때
            if (!response.ok) {
                const txt = await response.text();
                return { error: `Server responded ${response.status}: ${txt}` };
            }

            // 정상 JSON이면 파싱
            const data = await response.json();
            return data;
        } catch (err) {
            // 네트워크/크로스 도메인 문제 등 잡아냄
            return { error: String(err) };
        }
    }

};
