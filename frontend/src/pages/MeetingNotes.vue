<template>
  <div class="p-8 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">회의록 작성</h1>

    <!-- 작성 폼 -->
    <form @submit.prevent="saveNote" class="space-y-4 bg-white p-6 rounded shadow-sm">
      <div>
        <label class="block text-sm font-medium text-gray-700">제목</label>
        <input v-model="title" type="text" class="mt-1 block w-full border rounded p-2" placeholder="회의 제목" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">날짜</label>
          <input v-model="date" type="date" class="mt-1 block w-full border rounded p-2" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">참석자 (콤마로 구분)</label>
          <input v-model="attendees" type="text" class="mt-1 block w-full border rounded p-2" placeholder="홍길동, 김철수" />
        </div>
      </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">요약 / 메모</label>
          <textarea v-model="notes" rows="6" class="mt-1 block w-full border rounded p-2" placeholder="회의 주요 내용"></textarea>
        </div>

        <!-- 오디오 업로드: mp3 또는 wav 파일을 받아 전사(transcribe)합니다. -->
        <div>
          <label class="block text-sm font-medium text-gray-700">오디오 업로드 (mp3 / wav)</label>
          <input @change="onFileChange" accept="audio/*" type="file" class="mt-1 block" />
          <div v-if="audioUploading" class="text-sm text-gray-500 mt-1">업로드 및 전사 중...</div>
          <div v-else-if="audioMessage" class="text-sm text-gray-500 mt-1">{{ audioMessage }}</div>
        </div>

        <!-- 전사 결과와 요약 표시 -->
        <div v-if="transcribedText || transcribedSummary" class="mt-4 bg-gray-50 border p-4 rounded">
          <div v-if="transcribedText">
            <div class="font-semibold mb-1">전사 텍스트</div>
            <pre class="whitespace-pre-wrap bg-white p-3 rounded border text-sm">{{ transcribedText }}</pre>
            <div class="mt-2">
              <button class="px-3 py-1 text-sm bg-indigo-600 text-white rounded" @click="insertTranscript">메모에 전사 텍스트 삽입</button>
            </div>
          </div>

          <div v-if="transcribedSummary" class="mt-4">
            <div class="font-semibold mb-1">요약 (GPT-3.5)</div>
            <pre class="whitespace-pre-wrap bg-white p-3 rounded border text-sm">{{ transcribedSummary }}</pre>
            <div class="mt-2 flex gap-2">
              <button class="px-3 py-1 text-sm bg-green-600 text-white rounded" @click="insertSummary">요약을 메모에 삽입</button>
              <button class="px-3 py-1 text-sm bg-gray-200 rounded" @click="clearTranscriptData">지우기</button>
            </div>
          </div>
        </div>

      <div class="flex items-center space-x-2">
        <button class="px-4 py-2 bg-green-600 text-white rounded" :disabled="saving">저장</button>
        <button type="button" class="px-4 py-2 bg-gray-200 rounded" @click="clearForm">초기화</button>
      </div>
    </form>

    <!-- 저장된 회의록 리스트 -->
    <section class="mt-8">
      <h2 class="text-lg font-semibold mb-2">저장된 회의록</h2>
      <div v-if="notesList.length === 0" class="text-sm text-gray-500">저장된 회의록이 없습니다.</div>

      <ul class="space-y-3 mt-4">
        <li v-for="(n, idx) in notesList" :key="idx" class="border rounded p-3 bg-white">
          <div class="flex justify-between items-start">
            <div>
              <div class="font-semibold text-gray-800">{{ n.title || '(제목 없음)' }}</div>
              <div class="text-xs text-gray-500">{{ n.date }} · 참석자: {{ n.attendees }}</div>
            </div>
            <div class="flex items-center gap-2">
              <button class="px-2 py-1 text-sm bg-blue-600 text-white rounded" @click="viewNote(idx)">보기</button>
              <button class="px-2 py-1 text-sm bg-red-500 text-white rounded" @click="deleteNote(idx)">삭제</button>
            </div>
          </div>
          <p class="mt-2 text-sm text-gray-700">{{ n.notes }}</p>
          <div v-if="n.summary" class="mt-2 text-sm text-gray-600 bg-gray-50 p-2 rounded">요약: {{ n.summary }}</div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'meeting_notes'

const title = ref('')
const date = ref('')
const attendees = ref('')
import { API } from '../api/backend'

const notes = ref('')
const transcribedText = ref('')
const transcribedSummary = ref('')
const saving = ref(false)
const audioUploading = ref(false)
const audioMessage = ref('')
const notesList = ref([])

function loadNotes() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    notesList.value = raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error('load error', err)
    notesList.value = []
  }
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notesList.value))
}

function clearForm() {
  title.value = ''
  date.value = ''
  attendees.value = ''
  notes.value = ''
  transcribedText.value = ''
  transcribedSummary.value = ''
  audioMessage.value = ''
}

async function saveNote() {
  saving.value = true
  try {
    notesList.value.unshift({
      title: title.value,
      date: date.value,
      attendees: attendees.value,
      notes: notes.value,
      transcript: transcribedText.value,
      summary: transcribedSummary.value,
    })
    persist()
    clearForm()
  } finally {
    saving.value = false
  }
}

function insertTranscript() {
  if (!transcribedText.value) return
  notes.value = notes.value ? notes.value + '\n\n' + transcribedText.value : transcribedText.value
}

function insertSummary() {
  if (!transcribedSummary.value) return
  notes.value = notes.value ? notes.value + '\n\n' + transcribedSummary.value : transcribedSummary.value
}

function clearTranscriptData() {
  transcribedText.value = ''
  transcribedSummary.value = ''
  audioMessage.value = ''
}

// 오디오 파일 선택 핸들러
async function onFileChange(e) {
  const f = e.target.files?.[0]
  if (!f) return

  // 간단한 타입 검사
  if (!f.type.startsWith('audio/')) {
    audioMessage.value = '오디오 파일(mp3, wav)을 업로드하세요.'
    return
  }

  audioUploading.value = true
  audioMessage.value = ''
  try {
    const res = await API.uploadAudio(f)
    if (res.error) {
      audioMessage.value = `전사 실패: ${res.error}`
    } else if (res.text) {
      audioMessage.value = '전사 완료 — 텍스트와 요약을 아래에서 확인하세요.'
      // 전사결과와 요약을 상태로 저장
      transcribedText.value = res.text
      transcribedSummary.value = res.summary || ''
    } else {
      audioMessage.value = '전사 결과가 없습니다.'
    }
  } catch (err) {
    audioMessage.value = `업로드/전사 중 오류: ${err}`
  } finally {
    audioUploading.value = false
  }
}

function deleteNote(idx) {
  if (!confirm('정말 삭제하시겠습니까?')) return
  notesList.value.splice(idx, 1)
  persist()
}

function viewNote(idx) {
  const n = notesList.value[idx]
  alert(`제목: ${n.title || '(제목 없음)'}\n날짜: ${n.date}\n참석자: ${n.attendees}\n\n${n.notes}`)
}

onMounted(() => loadNotes())
</script>

<style scoped>
/* 기본적으로 Tailwind를 사용하므로 스타일은 최소화했습니다. */
</style>
