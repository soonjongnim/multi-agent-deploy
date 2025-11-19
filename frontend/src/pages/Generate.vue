<template>
  <!-- 전체 페이지 레이아웃: 헤더 + 메인 폼 + 결과 -->
  <div class="min-h-screen bg-gray-100 flex flex-col">

    <!-- 헤더: 간단한 타이틀/상태 표시 -->
    <header class="bg-white shadow-sm py-4 px-6 flex items-center justify-between">
      <div class="text-2xl font-bold text-gray-800">Site Generator</div>
      <div class="text-sm text-gray-500">Powered by AI</div>
    </header>

    <!-- 메인 컨테이너: 폼과 결과 카드 포함 -->
    <main class="flex-1 flex justify-center items-start py-12 px-4">
      <div class="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8">

        <!-- 타이틀 -->
        <h2 class="text-3xl font-semibold text-gray-800 mb-6">
          Create Your Website Instantly
        </h2>

        <!-- 입력 폼: prompt 입력 및 제출 -->
        <form @submit.prevent="handleGenerate" class="space-y-5">
          <label class="block">
            <span class="text-lg font-medium text-gray-700">Website Description</span>
            <!-- v-model로 prompt 상태 바인딩 -->
            <textarea
              v-model="prompt"
              rows="5"
              class="mt-2 w-full rounded-xl border border-gray-300 p-4 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-700 text-lg"
              placeholder="Tell me the website you want to generate..."
            ></textarea>
          </label>

          <!-- 제출 버튼: loading 상태에 따라 비활성화 -->
          <button
            type="submit"
            class="w-full py-3 rounded-xl text-white text-lg font-semibold transition bg-blue-600 hover:bg-blue-700"
            :disabled="loading"
          >
            {{ loading ? "Generating..." : "Generate Website" }}
          </button>
        </form>

        <!-- 에러 표시 영역 -->
        <div v-if="error" class="mt-6 bg-red-50 text-red-700 p-4 rounded-xl">
          ⚠️ {{ error }}
        </div>

        <!-- 결과 카드: API 응답을 보여줌 -->
        <div v-if="result" class="mt-10 bg-gray-50 border border-gray-200 rounded-2xl p-6">
          <h3 class="text-xl font-semibold mb-4">Result</h3>

          <!-- 결과 JSON을 예쁘게 출력 -->
          <pre class="whitespace-pre-wrap bg-white p-4 rounded-xl border text-sm">
{{ JSON.stringify(result, null, 2) }}
          </pre>

          <!-- 프리뷰 및 배포 버튼: result.preview_url이 있을 때만 표시 -->
          <div v-if="result.preview_url" class="mt-6 flex items-center">
            <!-- 새 탭으로 프리뷰 열기 -->
            <a
              :href="result.preview_url"
              target="_blank"
              class="px-4 py-2 rounded-xl bg-purple-600 text-white font-semibold text-lg hover:bg-purple-700 transition"
            >
              🔍 Open Preview
            </a>

            <!-- 배포 버튼: Vercel 등으로 배포 요청 -->
            <button
              @click="handleDeploy"
              class="ml-4 px-4 py-2 rounded-xl bg-green-600 text-white font-semibold text-lg hover:bg-green-700 transition"
              :disabled="loading"
            >
              🚀 Deploy to Vercel
            </button>
          </div>

          <!-- 배포 성공 출력 -->
          <div v-if="result.deploy_output" class="mt-6 p-4 bg-white border rounded-xl text-sm">
            <div class="font-semibold text-gray-800 mb-2">Deploy Output:</div>
            <pre class="whitespace-pre-wrap">{{ result.deploy_output }}</pre>
          </div>

          <!-- 배포 에러 출력 -->
          <div v-if="result.deploy_error" class="mt-6 p-4 bg-red-50 border border-red-300 rounded-xl text-sm text-red-700">
            <div class="font-semibold mb-2">Deploy Error:</div>
            <pre class="whitespace-pre-wrap">{{ result.deploy_error }}</pre>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
// Vue 3 Composition API의 ref를 사용하여 반응형 상태를 생성합니다.
import { ref } from "vue";
// API 호출 래퍼
import { API } from "../api/backend";

// 컴포넌트 상태 선언
const prompt = ref(""); // 사용자 입력
const loading = ref(false); // 요청 진행 상태
const result = ref(null); // 백엔드 응답 저장
const error = ref(null); // 에러 메시지

// 사이트 생성 핸들러: 백엔드 /generate 호출
async function handleGenerate() {
  error.value = null;
  result.value = null;

  if (!prompt.value.trim()) {
    error.value = "Please enter a website description.";
    return;
  }

  loading.value = true;

  try {
    // API.generateSite는 { prompt }를 받고 JSON을 반환합니다.
    const data = await API.generateSite({ prompt: prompt.value });
    result.value = data;
  } catch (err) {
    error.value = String(err);
  } finally {
    loading.value = false;
  }
}

// 배포 핸들러: preview_url을 백엔드에 보내 배포 요청
async function handleDeploy() {
  if (!result.value?.preview_url) {
    error.value = "Preview not available for deployment.";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const data = await API.deploySite({ preview_url: result.value.preview_url });

    if (data.deploy_error) {
      error.value = data.deploy_error;
    } else {
      // 배포 결과를 로컬 상태에 저장
      result.value.deploy_output = data.deploy_output;
      result.value.deploy_error = data.deploy_error;
      alert("Deploy Completed!");
    }
  } catch (err) {
    error.value = String(err);
  } finally {
    loading.value = false;
  }
}
</script>
