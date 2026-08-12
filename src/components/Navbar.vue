<script setup lang="ts">
import { Zap, Mail, User, X } from 'lucide-vue-next';
import { ref } from 'vue';

const showContactModal = ref(false);

const scrollTo = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
};
</script>

<template>
  <nav class="fixed top-5 left-1/2 -translate-x-1/2 z-50 w-full max-w-[1000px] px-4">
    <div class="bg-[#0d0d0d]/90 backdrop-blur-2xl border border-white/8 rounded-full px-2 py-2 flex items-center justify-between shadow-[0_8px_32px_rgba(0,0,0,0.6)]">
      <div class="flex items-center gap-2 pl-4">
        <Zap class="w-5 h-5 text-brand-orange fill-brand-orange" />
        <span class="font-black text-base tracking-tighter text-white">Swarm Agent</span>
      </div>

      <div class="hidden md:flex items-center gap-10 text-[13px] font-bold text-white/40">
        <a @click.prevent="scrollTo('technology')" href="#technology"
           class="hover:text-white transition-colors duration-200 cursor-pointer relative group">
          Technology
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </a>
        <a @click.prevent="scrollTo('architecture')" href="#architecture"
           class="hover:text-white transition-colors duration-200 cursor-pointer relative group">
          Architecture
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </a>
        <button @click="showContactModal = true"
           class="hover:text-white transition-colors duration-200 flex items-center gap-1.5 relative group cursor-pointer">
          <User class="w-3.5 h-3.5" />
          Contact
          <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-brand-orange rounded-full transition-all duration-300 group-hover:w-full"></span>
        </button>
      </div>

      <button
        @click="scrollTo('workspace-anchor')"
        class="relative overflow-hidden bg-brand-orange text-white px-8 py-3 rounded-full text-[13px] font-bold shadow-lg transition-all duration-300 active:scale-95 group hover:bg-orange-500">
        <span class="relative z-10">Get Started</span>
      </button>
    </div>

    <!-- Developer Contact Modal -->
    <div v-if="showContactModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md" @click.self="showContactModal = false">
      <div class="bg-[#111111] border border-white/12 rounded-3xl p-8 max-w-md w-full relative shadow-2xl space-y-6 text-left">
        <button @click="showContactModal = false" class="absolute top-6 right-6 text-white/40 hover:text-white transition-colors">
          <X class="w-5 h-5" />
        </button>

        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-brand-orange/10 border border-brand-orange/30 flex items-center justify-center text-brand-orange">
            <User class="w-6 h-6" />
          </div>
          <div>
            <h3 class="text-xl font-black text-white">Aswin Bino</h3>
            <p class="text-xs font-bold text-white/40 uppercase tracking-widest">Developer & AI Engineer</p>
          </div>
        </div>

        <div class="space-y-3 pt-2 text-sm">
          <div class="p-4 rounded-2xl bg-white/5 border border-white/8 flex items-center gap-3 text-white/70">
            <Mail class="w-4 h-4 text-brand-orange" />
            <span class="font-medium">Developer Contact: Aswin Bino</span>
          </div>
          <div class="p-4 rounded-2xl bg-white/5 border border-white/8 text-xs text-white/50 leading-relaxed">
            Project: Swarm Agent Orchestrator & AI Blog Writer<br/>
            Engineered with Pydantic AI, Vue 3, and Flask.
          </div>
        </div>

        <button @click="showContactModal = false" class="w-full py-3 bg-brand-orange text-white rounded-full font-bold text-xs uppercase tracking-widest hover:bg-orange-500 transition-colors">
          Close
        </button>
      </div>
    </div>
  </nav>
</template>
