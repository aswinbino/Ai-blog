<script setup lang="ts">
import { ChevronRight, ArrowRight } from 'lucide-vue-next';
defineEmits(['start']);

const scrollTo = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
};
</script>

<template>
  <section class="hero-section pt-40 pb-24 text-center px-4 relative overflow-hidden bg-[#080808]">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full" style="background: radial-gradient(circle, rgba(255,92,0,0.06) 0%, transparent 70%);"></div>
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
    </div>

    <div class="hero-content relative z-10 w-full max-w-6xl mx-auto">
      <div class="scroll-reveal inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-white/5 border border-white/8 mb-10">
        <div class="w-1.5 h-1.5 bg-brand-orange rounded-full animate-pulse"></div>
        <span class="text-[10px] uppercase font-black tracking-[0.3em] text-white/40">Agents Content Orchestration</span>
      </div>

      <h1 class="scroll-reveal text-[clamp(3.5rem,10vw,8rem)] font-black leading-[0.9] tracking-[-0.04em] text-white mb-10">
        The future of writing<br />is <span class="text-brand-orange">autonomous.</span>
      </h1>

      <p class="scroll-reveal text-lg md:text-xl text-white/30 max-w-2xl mx-auto mb-16 font-medium leading-relaxed">
        Leverage a collective of Pydantic AI agents to research, outline, and write
        high-performance long-form content for production-grade environments.
      </p>

      <div class="scroll-reveal flex flex-col sm:flex-row items-center justify-center gap-4">
        <button
          @click="$emit('start')"
          class="group relative bg-brand-orange text-white px-10 py-5 rounded-full font-black text-base flex items-center gap-2 transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(255,92,0,0.3)] active:scale-95 overflow-hidden hover:bg-orange-500"
        >
          <span class="relative z-10 flex items-center gap-2">
            Start Generating
            <ChevronRight class="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
          </span>
        </button>

        <button
          @click="scrollTo('architecture')"
          class="group relative px-10 py-5 rounded-full font-black text-base border border-white/12 bg-white/5 text-white/70 transition-all duration-300 hover:border-white/25 hover:bg-white/8 hover:text-white active:scale-95"
        >
          <span class="relative z-10">View Architecture</span>
        </button>
      </div>
    </div>
  </section>
</template>

