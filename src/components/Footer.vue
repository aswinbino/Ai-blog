<script setup lang="ts">
import { Zap } from 'lucide-vue-next';
</script>

<template>
  <footer class="py-16 px-6 border-t border-white/5 bg-[#080808]">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8 text-center md:text-left">

      <div class="flex items-center gap-2">
        <Zap class="w-4 h-4 text-brand-orange fill-brand-orange" />
        <span class="font-black text-sm tracking-tighter text-white">Swarm Agent</span>
      </div>

      <p class="text-[10px] font-black tracking-[0.2em] text-white/20 uppercase">
        © 2026 AI BLOG WRITER. DEVELOPED BY ASWIN BINO.
      </p>

      <div class="flex gap-8 text-[10px] uppercase font-black tracking-widest text-white/25">
        <a href="https://github.com/aswinbino/Ai-blog.git" target="_blank" class="hover:text-white transition-colors duration-200 relative group">
          Docs
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </a>
        <a href="#architecture" class="hover:text-white transition-colors duration-200 relative group">
          Architecture
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </a>
        <a href="https://github.com/aswinbino/Ai-blog.git" target="_blank" class="hover:text-white transition-colors duration-200 relative group">
          GitHub
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </a>
      </div>

    </div>
  </footer>
</template>

