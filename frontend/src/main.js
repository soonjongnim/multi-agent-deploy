// Vue 애플리케이션 엔트리 포인트
// - createApp: 루트 Vue 어플리케이션 인스턴스 생성
import { createApp } from 'vue'

// 루트 컴포넌트 (Single File Component)
import App from './App.vue'

// 라우터 설정을 가져옵니다 (vue-router)
import router from './router'

// 전역 스타일(예: Tailwind)을 불러옵니다
import './index.css'

// 애플리케이션 인스턴스 생성 및 마운트
const app = createApp(App)
app.use(router) // 라우터 플러그인 등록
app.mount('#app') // #app 엘리먼트에 Vue 앱 마운트
