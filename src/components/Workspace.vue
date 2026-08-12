<script setup lang="ts">
import { Send } from 'lucide-vue-next';
import { ref } from 'vue';

const props = defineProps<{
  modelValue: string;
  loading: boolean;
}>();

const emit = defineEmits(['update:modelValue', 'submit']);

const onInput = (e: Event) => {
  emit('update:modelValue', (e.target as HTMLInputElement).value);
};
</script>

<template>
  <section id="workspace" class="py-24 px-4 max-w-5xl mx-auto text-center">
    <div class="scroll-reveal mb-16">
      <h2 class="text-4xl md:text-6xl font-black tracking-tighter text-white mb-4">Workspace.</h2>
      <p class="text-white/30 font-bold text-base">Initialize the swarm with your directive.</p>
    </div>

    <div
      id="workspace-anchor"
      class="scroll-reveal relative max-w-3xl mx-auto group px-2 md:px-0"
    >
      <div class="flex flex-col md:flex-row items-center bg-[#111111] border border-white/8 rounded-[2rem] md:rounded-full shadow-[0_0_0_1px_rgba(255,255,255,0.04),0_20px_60px_-10px_rgba(0,0,0,0.6)] transition-all duration-300 focus-within:border-white/16 focus-within:shadow-[0_0_0_1px_rgba(255,255,255,0.08),0_20px_60px_-10px_rgba(0,0,0,0.8)] overflow-hidden">
        <input
          :value="modelValue"
          @input="onInput"
          @keyup.enter="$emit('submit')"
          class="w-full md:flex-1 h-16 md:h-20 px-8 bg-transparent border-none focus:outline-none text-base font-medium placeholder:text-white/20 text-white text-center md:text-left"
          placeholder="The Role of AI in Cybersecurity: Opportunities and Risks"
          :disabled="loading"
        />
        <div class="w-full md:w-auto p-2 md:p-3 md:pr-3">
          <button
            @click="$emit('submit')"
            :disabled="loading"
            class="w-full md:w-auto group/btn relative overflow-hidden h-12 md:h-14 bg-brand-orange text-white px-8 rounded-full flex items-center justify-center gap-3 font-bold text-sm hover:bg-orange-500 disabled:opacity-40 transition-all active:scale-95 shadow-lg"
          >
            <Send v-if="!loading" class="w-4 h-4 relative z-10 group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5 transition-transform duration-300" />
            <span class="relative z-10">{{ loading ? 'Deploying...' : 'Generate Blog' }}</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

