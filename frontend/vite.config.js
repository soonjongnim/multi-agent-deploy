// Vite 설정 파일
import { defineConfig } from 'vite'
// Vue 플러그인: SFC(.vue) 파일을 처리하도록 합니다.
import vue from '@vitejs/plugin-vue'

export default defineConfig({
	// 플러그인 배열에 vue를 추가하면 .vue 파일을 Vite가 빌드/번들링할 수 있습니다.
	plugins: [vue()],
})