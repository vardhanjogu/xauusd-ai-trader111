"use client";

import { useState, useEffect } from "react";
import { Activity, TrendingUp, Cpu, ShieldAlert, History, PlayCircle } from "lucide-react";

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState("overview");
    const [price, setPrice] = useState(2000.0);

    useEffect(() => {
        // Mock live price feed for visual validation
        const interval = setInterval(() => {
            setPrice(prev => prev + (Math.random() > 0.5 ? 0.5 : -0.5));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const tabs = [
        { id: "overview", label: "Overview", icon: Activity },
        { id: "trades", label: "Active Trades", icon: TrendingUp },
        { id: "ai", label: "AI Model", icon: Cpu },
        { id: "risk", label: "Risk Manager", icon: ShieldAlert },
        { id: "backtest", label: "Backtesting", icon: History },
    ];

    return (
        <div className="space-y-6">
            {/* Metrics Ribbon */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="panel flex flex-col justify-between">
                    <span className="text-gray-400 text-sm">Live Price (XAUUSD)</span>
                    <span className="text-3xl font-bold text-gold-500">${price.toFixed(2)}</span>
                </div>
                <div className="panel flex flex-col justify-between">
                    <span className="text-gray-400 text-sm">Active Signal</span>
                    <span className="text-2xl font-bold text-green-400 mt-2"><span className="badge-buy text-lg px-3 py-1">BUY (0.85)</span></span>
                </div>
                <div className="panel flex flex-col justify-between">
                    <span className="text-gray-400 text-sm">Daily PnL</span>
                    <span className="text-3xl font-bold text-green-400">+$420.50</span>
                </div>
                <div className="panel flex flex-col justify-between">
                    <span className="text-gray-400 text-sm">Risk Exposure</span>
                    <span className="text-3xl font-bold text-gold-400">1.2%</span>
                </div>
            </div>

            {/* Navigation Tabs */}
            <div className="flex space-x-2 border-b border-terminal-border overflow-x-auto pb-2">
                {tabs.map(tab => {
                    const Icon = tab.icon;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center space-x-2 px-4 py-2 rounded transition-colors whitespace-nowrap ${activeTab === tab.id
                                    ? "bg-terminal-panel border-t border-l border-r border-terminal-border text-gold-400"
                                    : "text-gray-400 hover:text-gray-200 hover:bg-terminal-panel/50 border border-transparent"
                                }`}
                        >
                            <Icon size={18} />
                            <span>{tab.label}</span>
                        </button>
                    )
                })}
            </div>

            {/* Tab Content Area */}
            <div className="panel min-h-[400px]">
                {activeTab === "overview" && (
                    <div className="space-y-4">
                        <h2 className="text-xl font-bold mb-4">System Overview</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="border border-terminal-border rounded p-4 bg-black/20">
                                <h3 className="text-gold-500 mb-2 font-semibold">Microservices Health</h3>
                                <ul className="space-y-2 font-mono text-sm">
                                    {['api_gateway', 'market_data', 'data_pipeline', 'ai_model', 'strategy_engine', 'risk_manager', 'execution', 'backtesting'].map(svc => (
                                        <li key={svc} className="flex justify-between border-b border-terminal-border/50 pb-1">
                                            <span className="text-gray-300">{svc}</span>
                                            <span className="text-green-400">Passing</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div className="border border-terminal-border rounded p-4 bg-black/20">
                                <h3 className="text-gold-500 mb-2 font-semibold">Recent Activity Log</h3>
                                <div className="font-mono text-xs space-y-2 text-gray-400">
                                    <p>[16:42:01] <span className="text-blue-400">INFO</span> Data Pipeline extracted 14 features.</p>
                                    <p>[16:42:02] <span className="text-blue-400">INFO</span> AI Model predicted BUY with 85% conf.</p>
                                    <p>[16:42:02] <span className="text-blue-400">INFO</span> Risk Manager validated exposure limits.</p>
                                    <p>[16:42:03] <span className="text-green-400">SUCCESS</span> Execution Engine placed order SIM_8A7B6C.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === "trades" && (
                    <div>
                        <h2 className="text-xl font-bold mb-4">Active & Recent Trades</h2>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="text-gray-400 border-b border-terminal-border">
                                    <tr>
                                        <th className="pb-3 text-gold-500">Ticket</th>
                                        <th className="pb-3 text-gold-500">Side</th>
                                        <th className="pb-3 text-gold-500">Volume</th>
                                        <th className="pb-3 text-gold-500">Entry</th>
                                        <th className="pb-3 text-gold-500">Current</th>
                                        <th className="pb-3 text-gold-500">S/L</th>
                                        <th className="pb-3 text-gold-500">T/P</th>
                                        <th className="pb-3 text-gold-500">PnL</th>
                                        <th className="pb-3 text-right text-gold-500">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-terminal-border">
                                    <tr className="hover:bg-black/20 transition-colors">
                                        <td className="py-3 font-mono">SIM_8A7B6C</td>
                                        <td className="py-3"><span className="badge-buy">BUY</span></td>
                                        <td className="py-3">1.5</td>
                                        <td className="py-3">2010.50</td>
                                        <td className="py-3 text-green-400 animate-pulse">{price.toFixed(2)}</td>
                                        <td className="py-3 text-red-400">2005.00</td>
                                        <td className="py-3 text-green-400">2021.50</td>
                                        <td className="py-3 font-bold text-green-400">+${((price - 2010.50) * 1.5 * 100).toFixed(2)}</td>
                                        <td className="py-3 text-right">
                                            <button className="bg-red-500/20 text-red-400 hover:bg-red-500/40 border border-red-500/30 px-3 py-1 rounded text-xs">
                                                CLOSE
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* Other tabs would go here based on user interaction in real app */}
                {activeTab !== "overview" && activeTab !== "trades" && (
                    <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                        <p>Section connected and ready for data stream initialization.</p>
                        <p className="text-sm mt-2 font-mono">Status: Awaiting WebSocket Feed ({activeTab})</p>
                    </div>
                )}

            </div>
        </div>
    );
}
