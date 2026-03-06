"use client";

import { useState, useEffect } from "react";
import Dashboard from "@/components/Dashboard";

export default function Home() {
  return (
    <main className="p-4 md:p-8 max-w-7xl mx-auto space-y-6">
      <header className="flex items-center justify-between border-b border-terminal-border pb-6">
        <div>
          <h1 className="text-3xl font-bold flex items-center space-x-3">
            <span className="text-gold-500">XAUUSD</span>
            <span className="bg-terminal-panel px-3 py-1 rounded text-lg border border-terminal-border">AI Trader</span>
          </h1>
          <p className="text-gray-400 mt-2">Production Intelligence & Execution Engine</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold tracking-wider text-green-400">SYSTEM ONLINE</span>
          </div>
        </div>
      </header>

      <Dashboard />
    </main>
  );
}
