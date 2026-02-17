# Mini YouTube Desktop App

A comprehensive Python desktop application built with Tkinter that simulates YouTube functionality while demonstrating various data structures and social media interactions.

## Screenshots

![Mini YouTube App Interface](screenshots/mini_youtube_interface.png)

*The Mini YouTube app interface showing the main video grid, category sidebar, and data structure visualizations in the Activity panel.*

## Features

### Core Functionality
- **Main Window**: "Mini YouTube" title with intuitive layout
- **Category Sidebar**: Hierarchical category navigation using Tree structure
- **Video Display**: Grid layout with video thumbnails and controls
- **Now Playing Section**: Shows currently playing video
- **Data Structure Visualization**: Real-time display of all data structures
- **Like/Dislike System**: Full YouTube-like engagement system
- **Comments System**: Add and view comments on videos
- **Search Functionality**: Find videos by title or category

### Data Structures Demonstrated

1. **Array/List** - Video Storage in Playlists & Comments
   - Store videos in playlists
   - Add/remove videos from playlists
   - Store comments for each video
   - Auto-managed "Liked Videos" playlist

2. **Stack (LIFO)** - Watch History
   - Last In, First Out principle
   - Most recently watched videos appear at top
   - Limited size with automatic cleanup

3. **Queue (FIFO)** - Upload Queue
   - First In, First Out processing
   - Simulates video upload processing
   - Visual representation of queue order

4. **Linked List** - Suggested Videos
   - Navigate through suggestions sequentially
   - Next/Reset functionality
   - Demonstrates linked node traversal

5. **Tree** - Category Hierarchy
   - Categories and subcategories
   - Hierarchical organization
   - Tree traversal for video collection

### Interactive Features

#### Video Controls
- **Play Video**: Updates "Now Playing" and adds to watch history (Stack)
- **Add to Playlist**: Choose existing playlist or create new one (Array operations)
- **Category Navigation**: Browse videos by category (Tree traversal)

#### Social Media Features
- **Like/Dislike Videos**: 
  - Toggle like/dislike status with visual feedback
  - Real-time count updates
  - Auto-management of "Liked Videos" playlist
  - Color-coded buttons (blue for liked, red for disliked)

- **Comments System**:
  - View existing comments with usernames and timestamps
  - Add new comments to videos
  - Comment like counts and engagement stats
  - Scrollable comments interface
  - Reply functionality (placeholder)

- **Engagement Statistics**:
  - Total likes across all videos
  - Total comments count
  - Personal liked videos count
  - Like-to-dislike ratios

#### Data Structure Operations
- **Watch History**: Automatic stack management with LIFO principle
- **Upload Queue**: Process uploads with FIFO queue operations
- **Suggestions**: Navigate linked list of recommended videos
- **Playlists**: Array operations (add, remove, display)

## Classes and Architecture

### Data Structure Classes
- `Video`: Enhanced video object with metadata, likes, dislikes, and comments
- `Comment`: Comment object with username, text, timestamp, and likes
- `HistoryStack`: Stack implementation for watch history (LIFO)
- `UploadQueue`: Queue implementation for uploads (FIFO)
- `SuggestedVideosList`: Linked list for video suggestions
- `CategoryTree`: Tree structure for category hierarchy
- `Playlist`: Array/List implementation for video playlists

### UI Classes
- `MiniYouTubeApp`: Main application class with complete UI management and social features

## How to Run

1. Ensure Python 3.x is installed
2. Run the application:
   ```bash
   python mini_youtube.py
   ```

## Usage Instructions

### Basic Operations
1. **Browse Categories**: Click on categories in the left sidebar (Tree navigation)
2. **Play Videos**: Click "▶ Play" on any video thumbnail
3. **Add to Playlist**: Click "+ Save" and select destination
4. **View History**: Watch history appears in right panel (Stack visualization)
5. **Process Uploads**: Click "Create" to handle pending uploads

### Social Media Features
1. **Like/Dislike Videos**: Click 👍 Like or 👎 buttons on video cards
2. **View Comments**: Click "💬 Comments" to open comments window
3. **Add Comments**: Type in comment box and click "Comment" to add
4. **View Liked Videos**: Click "👍 Liked videos" in sidebar to see all liked content
5. **Engagement Stats**: Check right panel for total likes, comments, and personal stats

### Data Structure Interactions
- **Stack**: Watch history updates automatically when playing videos
- **Queue**: Upload queue processes in FIFO order
- **Array**: Playlists show real-time video count and contents
- **Linked List**: Use "Next →" and "Reset" for suggestions navigation
- **Tree**: Category tree shows hierarchical organization with video counts

## Educational Value

This application demonstrates:
- **Practical Data Structure Usage**: Real-world applications of common data structures
- **GUI Programming**: Comprehensive Tkinter interface with multiple widgets
- **Object-Oriented Design**: Proper class structure and modularity
- **Event-Driven Programming**: Interactive GUI with responsive feedback
- **Visual Learning**: See data structures in action with immediate feedback

## Code Structure

The application is organized into clear sections:
1. **Data Structure Classes** (Lines 11-180): Core data structure implementations
2. **Main Application Class** (Lines 182-600): GUI and interaction logic
3. **UI Creation Methods** (Lines 240-350): Interface setup
4. **Event Handlers** (Lines 480-600): User interaction logic

Each data structure operation is clearly commented to show which structure is being used and how.