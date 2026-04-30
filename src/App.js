import React, { useState } from "react";
import "./App.css";

export default function FileSystemSimulator() {
  const TOTAL_BLOCKS = 64;
  const BLOCK_SIZE = 1024; // 1KB per block

  const [blocks, setBlocks] = useState(Array(TOTAL_BLOCKS).fill(null));
  const [files, setFiles] = useState({});
  const [directories, setDirectories] = useState({ "/": [] });
  const [currentDirectory, setCurrentDirectory] = useState("/");
  const [fileName, setFileName] = useState("");
  const [fileSize, setFileSize] = useState(1);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [theme, setTheme] = useState("dark");

  // Calculate statistics
  const usedBlocks = blocks.filter(block => block !== null).length;
  const freeBlocks = TOTAL_BLOCKS - usedBlocks;
  const totalSpace = TOTAL_BLOCKS * BLOCK_SIZE;
  const usedSpace = usedBlocks * BLOCK_SIZE;
  const freeSpace = freeBlocks * BLOCK_SIZE;
  const fragmentation = calculateFragmentation();

  function calculateFragmentation() {
    let fragments = 0;
    let inFile = false;
    for (let i = 0; i < blocks.length; i++) {
      if (blocks[i] !== null && !inFile) {
        inFile = true;
        fragments++;
      } else if (blocks[i] === null && inFile) {
        inFile = false;
      }
    }
    return fragments;
  }

  const createFile = () => {
    if (!fileName || fileSize < 1) return;

    let newBlocks = [...blocks];
    let contiguousBlocks = [];

    // Try to find contiguous space first
    for (let i = 0; i < newBlocks.length; i++) {
      if (newBlocks[i] === null) {
        contiguousBlocks.push(i);
        if (contiguousBlocks.length === fileSize) break;
      } else {
        contiguousBlocks = [];
      }
    }

    if (contiguousBlocks.length < fileSize) {
      // Fall back to any available blocks
      contiguousBlocks = [];
      for (let i = 0; i < newBlocks.length && contiguousBlocks.length < fileSize; i++) {
        if (newBlocks[i] === null) {
          newBlocks[i] = fileName;
          contiguousBlocks.push(i);
        }
      }
    } else {
      contiguousBlocks.forEach(i => newBlocks[i] = fileName);
    }

    if (contiguousBlocks.length < fileSize) {
      alert("Not enough space!");
      return;
    }

    setBlocks(newBlocks);
    setFiles({ ...files, [fileName]: contiguousBlocks });
    setDirectories({
      ...directories,
      [currentDirectory]: [...directories[currentDirectory], fileName]
    });
    setFileName("");
    setFileSize(1);
    setIsCreating(false);
  };

  const deleteFile = (name) => {
    let newBlocks = blocks.map((b) => (b === name ? null : b));
    let newFiles = { ...files };
    delete newFiles[name];

    let newDirectories = { ...directories };
    Object.keys(newDirectories).forEach(dir => {
      newDirectories[dir] = newDirectories[dir].filter(f => f !== name);
    });

    setBlocks(newBlocks);
    setFiles(newFiles);
    setDirectories(newDirectories);
    setSelectedFile(null);
  };

  const optimize = async () => {
    setIsOptimizing(true);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate processing time

    let newBlocks = Array(TOTAL_BLOCKS).fill(null);
    let index = 0;
    let newFiles = {};

    Object.keys(files).forEach((file) => {
      let size = files[file].length;
      let allocated = [];

      for (let i = 0; i < size; i++) {
        if (index < TOTAL_BLOCKS) {
          newBlocks[index] = file;
          allocated.push(index);
          index++;
        }
      }

      newFiles[file] = allocated;
    });

    setBlocks(newBlocks);
    setFiles(newFiles);
    setIsOptimizing(false);
  };

  const simulateCrash = () => {
    setFiles({});
    setDirectories({ "/": [] });
    setBlocks(Array(TOTAL_BLOCKS).fill(null));
    setSelectedFile(null);
  };

  const createDirectory = () => {
    const dirName = prompt("Enter directory name:");
    if (dirName && !directories[dirName]) {
      setDirectories({
        ...directories,
        [dirName]: [],
        [currentDirectory]: [...directories[currentDirectory], dirName]
      });
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'} transition-colors duration-300 animate-fade-in`}>
      <div className="flex flex-col items-center justify-center min-h-screen px-4 sm:px-6 lg:px-8 py-8">
        <div className="w-full max-w-7xl mx-auto">
          {/* Header */}
          <header className={`${theme === 'dark' ? 'bg-gray-800 backdrop-blur-glass-dark' : 'bg-white backdrop-blur-glass'} shadow-hard border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'} animate-slide-in rounded-4xl mb-8`}>
            <div className="flex justify-between items-center p-6">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-4xl flex items-center justify-center shadow-glow-blue animate-float">
                <span className="text-white font-bold text-lg">FS</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-shadow">File System Simulator</h1>
                <p className="text-sm opacity-75">Advanced Disk Management</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className={`p-3 rounded-4xl ${theme === 'dark' ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'} transition-bounce focus-ring`}
              >
                {theme === 'dark' ? '☀️' : '🌙'}
              </button>
              <button
                onClick={() => setShowStats(!showStats)}
                className={`px-4 py-2 rounded-4xl font-medium transition-smooth focus-ring ${
                  theme === 'dark' ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-200 hover:bg-gray-300'
                } ${showStats ? 'animate-glow' : ''}`}
              >
                📊
              </button>
            </div>
          </div>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - File Operations */}
          <div className="lg:col-span-1">
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-4xl shadow-medium p-6 animate-slide-in`}>
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <span className="mr-2 animate-bounce-gentle">📁</span>
                File Operations
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">File Name</label>
                  <input
                    type="text"
                    placeholder="Enter file name"
                    value={fileName}
                    onChange={(e) => setFileName(e.target.value)}
                    className={`w-full px-3 py-2 rounded-4xl border transition-smooth focus-ring ${
                      theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
                    }`}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Size (blocks)</label>
                  <input
                    type="number"
                    min="1"
                    max={freeBlocks}
                    value={fileSize}
                    onChange={(e) => setFileSize(parseInt(e.target.value) || 1)}
                    className={`w-full px-3 py-2 rounded-4xl border transition-smooth focus-ring ${
                      theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
                    }`}
                  />
                </div>

                <div className="flex space-x-2">
                  <button
                    onClick={() => setIsCreating(true)}
                    disabled={isCreating || freeBlocks < fileSize}
                    className={`flex-1 px-4 py-2 rounded-4xl font-medium transition-bounce focus-ring ${
                      freeBlocks < fileSize
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'btn-primary text-white'
                    }`}
                  >
                    {isCreating ? 'Creating...' : 'Create File'}
                  </button>
                  <button
                    onClick={createDirectory}
                    className="px-4 py-2 btn-secondary text-white rounded-4xl font-medium transition-bounce focus-ring"
                  >
                    📁 New Dir
                  </button>
                </div>

                <div className="border-t pt-4 space-y-2">
                  <button
                    onClick={optimize}
                    disabled={isOptimizing}
                    className={`w-full px-4 py-2 rounded-4xl font-medium transition-bounce focus-ring ${
                      isOptimizing
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-purple-600 to-purple-800 hover:from-purple-700 hover:to-purple-900 text-white shadow-glow-purple'
                    }`}
                  >
                    {isOptimizing ? 'Optimizing...' : '🧹 Defragment'}
                  </button>

                  <button
                    onClick={simulateCrash}
                    className="w-full px-4 py-2 bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 text-white rounded-4xl font-medium transition-bounce focus-ring shadow-glow-red"
                  >
                    💥 Simulate Crash
                  </button>
                </div>
              </div>
            </div>

            {/* Statistics Panel */}
            {showStats && (
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6 mt-6`}>
                <h3 className="text-lg font-semibold mb-4">📊 System Statistics</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span>Total Space:</span>
                    <span className="font-mono">{formatBytes(totalSpace)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Used Space:</span>
                    <span className="font-mono text-blue-400">{formatBytes(usedSpace)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Free Space:</span>
                    <span className="font-mono text-green-400">{formatBytes(freeSpace)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Files:</span>
                    <span className="font-mono">{Object.keys(files).length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Fragmentation:</span>
                    <span className="font-mono text-yellow-400">{fragmentation} fragments</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Usage:</span>
                    <span className="font-mono">{((usedBlocks / TOTAL_BLOCKS) * 100).toFixed(1)}%</span>
                  </div>
                  {/* Disk Usage Bar */}
                  <div className="mt-4">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Disk Usage</span>
                      <span>{((usedBlocks / TOTAL_BLOCKS) * 100).toFixed(1)}%</span>
                    </div>
                    <div className={`w-full h-3 rounded-full overflow-hidden ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500 ease-out"
                        style={{ width: `${(usedBlocks / TOTAL_BLOCKS) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Center Panel - File Explorer */}
          <div className="lg:col-span-2">
            <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-4xl shadow-medium p-6 animate-fade-in`}>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold flex items-center">
                  <span className="mr-2 animate-bounce-gentle">🗂️</span>
                  File Explorer
                </h2>
                <div className="text-sm opacity-75">
                  Current Directory: <span className="font-mono bg-gradient-to-r from-blue-200 to-purple-200 dark:from-blue-800 dark:to-purple-800 px-3 py-1 rounded-4xl text-shadow">{currentDirectory}</span>
                </div>
              </div>

              {/* Directory Navigation */}
              <div className="mb-4">
                <div className="flex flex-wrap gap-2">
                  {Object.keys(directories).map(dir => (
                    <button
                      key={dir}
                      onClick={() => setCurrentDirectory(dir)}
                      className={`directory-button px-3 py-2 rounded-4xl text-sm font-medium focus-ring ${
                        currentDirectory === dir
                          ? 'active'
                          : theme === 'dark'
                            ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                            : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                      }`}
                    >
                      📁 {dir}
                    </button>
                  ))}
                </div>
              </div>

              {/* Files List */}
              <div className="space-y-2">
                {directories[currentDirectory]?.map((item, index) => {
                  const isFile = files[item];
                  return (
                    <div
                      key={index}
                      onClick={() => setSelectedFile(selectedFile === item ? null : item)}
                      className={`file-item p-4 rounded-4xl cursor-pointer transition-smooth focus-ring ${
                        selectedFile === item
                          ? 'selected'
                          : theme === 'dark' ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-50 hover:bg-gray-100'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <span className="text-lg animate-float">{isFile ? '📄' : '📁'}</span>
                          <div>
                            <div className="font-medium text-shadow">{item}</div>
                            {isFile && (
                              <div className="text-sm opacity-75 font-mono">
                                {files[item].length} blocks • {formatBytes(files[item].length * BLOCK_SIZE)}
                              </div>
                            )}
                          </div>
                        </div>
                        {isFile && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteFile(item);
                            }}
                            className="text-red-500 hover:text-red-700 p-2 rounded-4xl transition-bounce focus-ring hover:shadow-glow-red"
                          >
                            🗑️
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
                {directories[currentDirectory]?.length === 0 && (
                  <div className="text-center py-12 text-gray-500 animate-fade-in">
                    <span className="text-6xl mb-4 block animate-bounce-gentle">📂</span>
                    <p className="text-lg">This directory is empty</p>
                    <p className="text-sm opacity-75">Create some files to get started!</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Disk Visualization */}
        <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-4xl shadow-hard p-6 mt-8 animate-fade-in bg-disk-pattern w-full`}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold flex items-center text-shadow-lg">
              <span className="mr-2 animate-spin-slow">💾</span>
              Disk Blocks ({TOTAL_BLOCKS} total)
            </h2>
            <div className="text-sm opacity-75 bg-gradient-to-r from-green-200 to-blue-200 dark:from-green-800 dark:to-blue-800 px-3 py-1 rounded-4xl">
              <span className="text-green-600 dark:text-green-400 font-medium">{freeBlocks} free</span> • <span className="text-blue-600 dark:text-blue-400 font-medium">{usedBlocks} used</span>
            </div>
          </div>

          <div className="grid grid-cols-8 md:grid-cols-16 gap-1 mb-4">
            {blocks.map((block, i) => (
              <div
                key={i}
                className={`disk-block h-8 w-8 rounded-sm flex items-center justify-center text-xs font-mono ${
                  block
                    ? 'bg-gradient-to-br from-blue-500 to-blue-700 text-white shadow-glow-blue'
                    : theme === 'dark'
                      ? 'bg-gray-600 hover:bg-gray-500'
                      : 'bg-gray-300 hover:bg-gray-400'
                } ${isOptimizing ? 'animate-pulse-slow' : ''}`}
                title={block ? `Block ${i}: ${block}` : `Block ${i}: Free`}
              >
                {block ? block.slice(0, 2) : ''}
              </div>
            ))}
          </div>

          <div className="flex flex-wrap gap-4 text-sm">
            <div className="flex items-center space-x-2 bg-gradient-to-r from-blue-100 to-blue-200 dark:from-blue-900 dark:to-blue-800 px-3 py-1 rounded-4xl">
              <div className="w-4 h-4 bg-gradient-to-br from-blue-500 to-blue-700 rounded animate-pulse-slow"></div>
              <span className="font-medium">Allocated Blocks</span>
            </div>
            <div className="flex items-center space-x-2 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 px-3 py-1 rounded-4xl">
              <div className={`w-4 h-4 rounded ${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-300'}`}></div>
              <span className="font-medium">Free Blocks</span>
            </div>
            {isOptimizing && (
              <div className="flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-purple-200 dark:from-purple-900 dark:to-purple-800 px-3 py-1 rounded-4xl animate-glow">
                <div className="w-4 h-4 bg-gradient-to-br from-purple-500 to-purple-700 rounded animate-spin-slow"></div>
                <span className="font-medium">Defragmenting...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Create File Modal */}
      {isCreating && (
        <div className="fixed inset-0 modal-overlay flex items-center justify-center z-50">
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-4xl shadow-hard p-6 max-w-md w-full mx-4 modal-content`}>
            <h3 className="text-lg font-semibold mb-4 flex items-center text-shadow">
              <span className="mr-2 animate-bounce-gentle">📄</span>
              Create New File
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">File Name</label>
                <input
                  type="text"
                  value={fileName}
                  onChange={(e) => setFileName(e.target.value)}
                  className={`w-full px-3 py-2 rounded-4xl border transition-smooth focus-ring ${
                    theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
                  }`}
                  placeholder="Enter file name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Size (blocks)</label>
                <input
                  type="number"
                  min="1"
                  max={freeBlocks}
                  value={fileSize}
                  onChange={(e) => setFileSize(parseInt(e.target.value) || 1)}
                  className={`w-full px-3 py-2 rounded-4xl border transition-smooth focus-ring ${
                    theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
                  }`}
                />
              </div>
            </div>
            <div className="flex space-x-3 mt-6">
              <button
                onClick={createFile}
                disabled={!fileName || fileSize < 1 || freeBlocks < fileSize}
                className={`flex-1 px-4 py-2 rounded-4xl font-medium transition-bounce focus-ring ${
                  !fileName || fileSize < 1 || freeBlocks < fileSize
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'btn-primary text-white'
                }`}
              >
                Create
              </button>
              <button
                onClick={() => setIsCreating(false)}
                className={`px-4 py-2 rounded-4xl font-medium transition-bounce focus-ring ${theme === 'dark' ? 'bg-gray-600 hover:bg-gray-500' : 'bg-gray-300 hover:bg-gray-400'}`}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}
