<template>
  <!-- 홈 페이지 템플릿: 간단한 안내 및 라우터 링크 -->
  <div class="p-8">
    <!-- 페이지 제목 -->
    <h1 class="text-2xl font-bold mb-4">Multi-Agent Deploy (Vue)</h1>
    <!-- 설명 문구 -->
    <p class="mb-4">Welcome — generate sites from prompts and deploy them automatically.</p>

    <!-- 네비게이션 버튼: 라우터 링크로 페이지 전환 -->
    <div class="space-x-2">
      <router-link to="/generate" class="px-4 py-2 bg-blue-600 text-white rounded">Generate</router-link>
      <router-link to="/deploy" class="px-4 py-2 bg-gray-200 rounded">Deploy</router-link>
      <!-- 회의록 작성 버튼 추가 -->
      <router-link to="/meetings" class="px-4 py-2 bg-indigo-600 text-white rounded">회의록 작성</router-link>
    </div>
  </div>
</template>

<script setup>
// Home 컴포넌트는 로직이 없으므로 빈 상태입니다.
</script>
