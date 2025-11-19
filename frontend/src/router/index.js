// Vue Router 설정 파일
import { createRouter, createWebHistory } from 'vue-router'

// 페이지 컴포넌트 임포트
import Home from '../pages/Home.vue'
import Generate from '../pages/Generate.vue'
import Deploy from '../pages/Deploy.vue'

// 라우트 배열 정의: 각 경로에 매칭되는 컴포넌트를 지정합니다.
const routes = [
  { path: '/', component: Home },
  { path: '/generate', component: Generate },
  { path: '/deploy', component: Deploy },
]

// createRouter로 라우터 인스턴스 생성
const router = createRouter({
  history: createWebHistory(), // HTML5 히스토리 모드 사용
  routes,
})

export default router
