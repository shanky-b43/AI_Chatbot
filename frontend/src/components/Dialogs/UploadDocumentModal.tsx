import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Loader2, UploadCloud, FileText } from 'lucide-react';
import { analyzeDocument, ingestDocument } from '@/api/documentApi';

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const UploadDocumentModal = ({ open, onOpenChange }: Props) => {
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<{
    filename: string;
    tmp_path: string;
    workflow: string;
    type: string;
  } | null>(null);
  const [ingesting, setIngesting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const supportedFormats = ".txt, .md, .pdf, .csv, .docx, .doc, .xls, .xlsx, .jpg, .jpeg, .png";

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setAnalysisResult(null);
      setError(null);
      setSuccess(false);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setAnalyzing(true);
    setError(null);
    try {
      const res = await analyzeDocument(file);
      setAnalysisResult(res);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to analyze document.");
    } finally {
      setAnalyzing(false);
    }
  };

  const handleIngest = async () => {
    if (!analysisResult) return;
    setIngesting(true);
    setError(null);
    try {
      await ingestDocument(analysisResult.filename, analysisResult.tmp_path, analysisResult.workflow);
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to ingest document.");
    } finally {
      setIngesting(false);
    }
  };

  const resetAndClose = () => {
    setFile(null);
    setAnalysisResult(null);
    setError(null);
    setSuccess(false);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={(val) => { if (!val) resetAndClose(); else onOpenChange(val); }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Upload Knowledge Document</DialogTitle>
          <DialogDescription>
            Upload a document to train the AI. It will be automatically categorized.
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col items-center justify-center space-y-4 py-4">
          {!analysisResult && !success && (
            <>
              <div className="w-full">
                <label
                  htmlFor="file-upload"
                  className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-zinc-300 dark:border-zinc-700 rounded-xl cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <UploadCloud className="w-8 h-8 mb-2 text-zinc-500" />
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">
                      {file ? <span className="font-semibold text-zinc-900 dark:text-zinc-100">{file.name}</span> : "Click to select a file"}
                    </p>
                  </div>
                  <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept=".txt,.md,.pdf,.csv,.docx,.doc,.xls,.xlsx,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
              
              <div className="text-xs text-zinc-500 text-center w-full">
                Supported formats:<br />
                <span className="font-mono">{supportedFormats}</span>
              </div>

              {error && <p className="text-sm text-red-500 font-medium">{error}</p>}

              <Button
                onClick={handleAnalyze}
                disabled={!file || analyzing}
                className="w-full"
              >
                {analyzing ? (
                  <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Analyzing...</>
                ) : (
                  "Analyze Document"
                )}
              </Button>
            </>
          )}

          {analysisResult && !success && (
            <div className="w-full space-y-4">
              <div className="p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <div className="flex items-center space-x-3 mb-2">
                  <FileText className="w-5 h-5 text-blue-500" />
                  <span className="font-medium truncate">{analysisResult.filename}</span>
                </div>
              </div>

              {error && <p className="text-sm text-red-500 font-medium">{error}</p>}

              <DialogFooter className="flex space-x-2 sm:space-x-0">
                <Button variant="outline" onClick={() => setAnalysisResult(null)} disabled={ingesting}>
                  Cancel
                </Button>
                <Button onClick={handleIngest} disabled={ingesting}>
                  {ingesting ? (
                    <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Ingesting...</>
                  ) : (
                    "Confirm & Ingest"
                  )}
                </Button>
              </DialogFooter>
            </div>
          )}

          {success && (
            <div className="flex flex-col items-center justify-center py-6 space-y-3">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                <UploadCloud className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="font-medium text-lg">Upload Successful!</h3>
              <p className="text-sm text-zinc-500 text-center">
                The document has been securely stored and ingested into the {analysisResult?.workflow} knowledge base.
              </p>
              <Button onClick={resetAndClose} className="mt-4 w-full">
                Close
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
