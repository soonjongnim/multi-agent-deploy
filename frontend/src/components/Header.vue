<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold text-gray-800">SiteGenerator</router-link>
          <nav class="ml-6 hidden md:flex space-x-4">
            <router-link to="/" class="text-gray-600 hover:text-gray-900">Home</router-link>
            <router-link to="/generate" class="text-gray-600 hover:text-gray-900">Generate</router-link>
            <router-link to="/preview" class="text-gray-600 hover:text-gray-900">Preview</router-link>
            <router-link to="/deploy" class="text-gray-600 hover:text-gray-900">Deploy</router-link>
          </nav>
        </div>

        <div class="flex items-center space-x-3">
          <a href="#" class="text-sm text-gray-500 hover:text-gray-700">Docs</a>
          <button class="px-3 py-1 rounded-md bg-blue-600 text-white text-sm hover:bg-blue-700">Sign in</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
// 이 헤더는 애플리케이션 전체에서 사용되는 공통 헤더입니다.
// 라우터 링크를 통해 페이지 전환을 제공합니다.
</script>

<style scoped>
/* 필요한 추가 스타일은 여기 추가하세요. 대부분은 Tailwind로 처리됩니다. */
</style>

