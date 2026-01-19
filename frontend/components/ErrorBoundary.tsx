import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error("Uncaught error:", error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-[#0b0e11] flex items-center justify-center p-6 text-white text-center">
                    <div className="max-w-md space-y-6">
                        <div className="w-20 h-20 bg-red-500/10 rounded-3xl flex items-center justify-center mx-auto mb-6">
                            <i className="fas fa-exclamation-triangle text-red-500 text-3xl"></i>
                        </div>
                        <h1 className="text-2xl font-black uppercase tracking-tighter">System Error Detected</h1>
                        <p className="text-gray-400 text-sm leading-relaxed">
                            TradeSense AI Core has encountered a critical rendering error. This usually happens when market data or library dependencies fail to initialize.
                        </p>
                        <div className="bg-black/50 p-4 rounded-xl text-left overflow-auto max-h-40 border border-white/5">
                            <code className="text-[10px] text-red-400 font-mono">{this.state.error?.toString()}</code>
                        </div>
                        <button
                            onClick={() => window.location.reload()}
                            className="px-8 py-4 bg-yellow-500 text-black font-black rounded-xl uppercase tracking-widest text-xs hover:bg-yellow-400 transition-all"
                        >
                            Reload System
                        </button>
                    </div>
                </div>
            );
        }

        return this.children;
    }

    // Custom getter for children to avoid direct access errors in some environments
    private get children() {
        return this.props.children;
    }
}

export default ErrorBoundary;
