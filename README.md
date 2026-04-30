# File System Simulator

A fully customized, responsive file system simulator built with React. This application provides an interactive visualization of disk block allocation, file management, and system optimization with a modern, professional UI.

## 🚀 Features

### Core Functionality
- **File Creation**: Create files with custom names and sizes
- **Directory Management**: Create and navigate through directories
- **File Deletion**: Remove files from the system
- **Disk Defragmentation**: Optimize file placement to reduce fragmentation
- **System Crash Simulation**: Reset the entire file system

### Advanced Features
- **Real-time Statistics**: Monitor disk usage, fragmentation levels, and system metrics
- **Visual Disk Blocks**: Interactive 64-block disk visualization with hover effects
- **File Explorer**: Modern file browser interface with directory navigation
- **Dark/Light Theme**: Toggle between themes for comfortable viewing
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Progress Indicators**: Visual feedback for long-running operations

### UI/UX Highlights
- **Modern Design**: Clean, professional interface with smooth animations
- **Interactive Elements**: Hover effects, transitions, and visual feedback
- **Modal Dialogs**: Elegant file creation interface
- **Real-time Updates**: Live statistics and disk usage visualization
- **Accessibility**: Proper contrast ratios and keyboard navigation

## 🛠️ Technical Stack

- **React 19**: Latest React with hooks for state management
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **JavaScript ES6+**: Modern JavaScript features
- **Create React App**: Zero-configuration React application setup

## 📊 System Specifications

- **Total Blocks**: 64 blocks
- **Block Size**: 1KB per block
- **Total Capacity**: 64KB
- **Allocation Strategy**: First-fit with contiguous block preference
- **File System Type**: Contiguous allocation with defragmentation support

## 🎯 Usage

1. **Create Files**: Enter a file name and size, then click "Create File"
2. **Create Directories**: Click "New Dir" to create folder structures
3. **Navigate**: Click on directory buttons to switch between folders
4. **Delete Files**: Click the trash icon next to any file
5. **Defragment**: Use "Defragment" to optimize disk space
6. **Monitor**: Click the stats button to view system metrics
7. **Theme Toggle**: Switch between light and dark modes

## 🔧 Development

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation
```bash
npm install
```

### Running the Application
```bash
npm start
```

The application will open at [http://localhost:3000](http://localhost:3000)

### Building for Production
```bash
npm run build
```

## 📈 Performance Features

- **Efficient Rendering**: Optimized React components with minimal re-renders
- **Smooth Animations**: CSS transitions and transforms for fluid interactions
- **Responsive Layout**: Adaptive grid system that works on all screen sizes
- **Memory Efficient**: Smart state management to prevent memory leaks

## 🎨 Design Philosophy

The File System Simulator combines educational value with modern web design principles:

- **Educational**: Teaches file system concepts through interactive visualization
- **Professional**: Enterprise-grade UI suitable for technical demonstrations
- **Accessible**: High contrast ratios and intuitive navigation
- **Performant**: Smooth 60fps animations and responsive interactions

## 🚀 Future Enhancements

- File content editing and viewing
- Drag-and-drop file operations
- Multiple disk volumes
- File permissions and security
- Backup and restore functionality
- Performance benchmarking tools

---

Built with ❤️ using React and Tailwind CSS

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
