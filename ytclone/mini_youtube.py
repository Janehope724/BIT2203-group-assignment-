"""
Mini YouTube Desktop App using Tkinter
Demonstrates various data structures: Arrays, Stacks, Queues, Linked Lists, and Trees
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import random
import os
import threading
import subprocess
import platform
import time
import cv2
import numpy as np
from PIL import Image, ImageTk

# ====================
# DATA STRUCTURE CLASSES
# ====================

class Comment:
    """Represents a comment on a video"""
    def __init__(self, username, text, timestamp=None):
        self.username = username
        self.text = text
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.likes = random.randint(0, 50)  # Comment likes
    
    def __str__(self):
        return f"{self.username}: {self.text}"

class Video:
    """Represents a video with basic metadata, likes, and comments"""
    def __init__(self, title, category, duration, thumbnail_color="lightblue", file_path=None):
        self.title = title
        self.category = category
        self.duration = duration
        self.thumbnail_color = thumbnail_color
        self.file_path = file_path  # Path to actual video file
        self.views = random.randint(100, 10000)
        self.upload_date = datetime.now().strftime("%Y-%m-%d")
        
        # Like/Dislike functionality
        self.likes = random.randint(50, 2000)
        self.dislikes = random.randint(5, 200)
        self.user_reaction = None  # None, 'like', or 'dislike'
        
        # Comments functionality
        self.comments = []  # List of Comment objects
        self.generate_sample_comments()
    
    def generate_sample_comments(self):
        """Generate some sample comments for each video"""
        sample_comments = [
            ("TechGuru99", "Great video! Really helpful!"),
            ("VideoLover", "Thanks for sharing this content"),
            ("RandomUser", "Could you make a follow-up video?"),
            ("LearnMore", "This explained everything perfectly"),
            ("QuickWatch", "Subscribed after watching this!"),
        ]
        
        # Add 2-4 random comments
        num_comments = random.randint(2, 4)
        selected_comments = random.sample(sample_comments, num_comments)
        
        for username, text in selected_comments:
            self.comments.append(Comment(username, text))
    
    def add_comment(self, username, text):
        """Add a new comment to the video"""
        comment = Comment(username, text)
        self.comments.append(comment)
        return comment
    
    def toggle_like(self):
        """Toggle like status and update counts"""
        if self.user_reaction == 'like':
            # Unlike
            self.user_reaction = None
            self.likes -= 1
        else:
            # Like (remove dislike if exists)
            if self.user_reaction == 'dislike':
                self.dislikes -= 1
            self.user_reaction = 'like'
            self.likes += 1
    
    def toggle_dislike(self):
        """Toggle dislike status and update counts"""
        if self.user_reaction == 'dislike':
            # Remove dislike
            self.user_reaction = None
            self.dislikes -= 1
        else:
            # Dislike (remove like if exists)
            if self.user_reaction == 'like':
                self.likes -= 1
            self.user_reaction = 'dislike'
            self.dislikes += 1
    
    def get_like_ratio(self):
        """Get like to dislike ratio as percentage"""
        total = self.likes + self.dislikes
        if total == 0:
            return 0
        return (self.likes / total) * 100
    
    def __str__(self):
        return f"{self.title} ({self.duration})"

class HistoryStack:
    """Stack implementation for watch history (LIFO - Last In, First Out)"""
    def __init__(self, max_size=10):
        self.stack = []  # LIST used as STACK data structure
        self.max_size = max_size
    
    def push(self, video):
        """Add video to top of history stack"""
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # Remove oldest if max size reached
        self.stack.append(video)
    
    def pop(self):
        """Remove and return most recent video (LIFO)"""
        return self.stack.pop() if self.stack else None
    
    def peek(self):
        """View most recent video without removing"""
        return self.stack[-1] if self.stack else None
    
    def get_all(self):
        """Return all history items (most recent first)"""
        return list(reversed(self.stack))

class UploadQueue:
    """Queue implementation for upload simulation (FIFO - First In, First Out)"""
    def __init__(self):
        self.queue = []  # LIST used as QUEUE data structure
    
    def enqueue(self, video):
        """Add video to end of upload queue"""
        self.queue.append(video)
    
    def dequeue(self):
        """Remove and return first video in queue (FIFO)"""
        return self.queue.pop(0) if self.queue else None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def get_all(self):
        """Return all queued items"""
        return self.queue.copy()

class SuggestionNode:
    """Node class for Linked List implementation"""
    def __init__(self, video):
        self.video = video
        self.next = None

class SuggestedVideosList:
    """Linked List implementation for suggested videos navigation"""
    def __init__(self):
        self.head = None
        self.current = None
    
    def add_suggestion(self, video):
        """Add video to suggestions linked list"""
        new_node = SuggestionNode(video)
        if not self.head:
            self.head = new_node
            self.current = new_node
        else:
            # Add to end of list
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
    
    def get_current(self):
        """Get current suggested video"""
        return self.current.video if self.current else None
    
    def next_suggestion(self):
        """Move to next suggestion in linked list"""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.video
        return None
    
    def reset(self):
        """Reset to first suggestion"""
        self.current = self.head
        return self.get_current()

class CategoryTree:
    """Tree implementation for categories hierarchy"""
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []  # LIST of child categories
        self.videos = []    # ARRAY/LIST of videos in this category
    
    def add_child_category(self, name):
        """Add subcategory to this category"""
        child = CategoryTree(name, self)
        self.children.append(child)
        return child
    
    def add_video(self, video):
        """Add video to this category"""
        self.videos.append(video)
    
    def get_all_videos(self):
        """Get all videos in this category and subcategories (tree traversal)"""
        all_videos = self.videos.copy()
        for child in self.children:
            all_videos.extend(child.get_all_videos())
        return all_videos

class Playlist:
    """Array/List implementation for playlists"""
    def __init__(self, name):
        self.name = name
        self.videos = []  # ARRAY/LIST data structure for storing videos
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
    
    def add_video(self, video):
        """Add video to playlist array"""
        if video not in self.videos:
            self.videos.append(video)
            return True
        return False
    
    def remove_video(self, video):
        """Remove video from playlist array"""
        if video in self.videos:
            self.videos.remove(video)
            return True
        return False
    
    def get_videos(self):
        """Return all videos in playlist"""
        return self.videos.copy()
    
    def shuffle(self):
        """Shuffle playlist order"""
        random.shuffle(self.videos)

# ====================
# MAIN APPLICATION CLASS
# ====================

class MiniYouTubeApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_data_structures()
        self.create_sample_data()
        self.setup_ui()
        self.update_displays()
    
    def setup_window(self):
        """Configure main window"""
        self.root.title("YouTube")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f0f0f")  # YouTube dark theme
        self.root.minsize(1200, 700)
        
        # Set window icon and state
        self.root.state('zoomed')  # Maximize window for clean look
    
    def initialize_data_structures(self):
        """Initialize all data structures"""
        # Stack for watch history
        self.watch_history = HistoryStack(max_size=10)
        
        # Queue for uploads
        self.upload_queue = UploadQueue()
        
        # Linked list for suggestions
        self.suggestions = SuggestedVideosList()
        
        # Tree for categories
        self.root_category = CategoryTree("All Videos")
        
        # Array/Lists for playlists
        self.playlists = {}  # Dictionary containing playlist objects
        
        # Currently playing video
        self.current_video = None
    
    def create_sample_data(self):
        """Create sample videos and organize them using data structures"""
        # Create sample videos - some with file paths for real playback
        sample_videos = [
            Video("Mini YouTube Test Video", "Demo", "0:05", "lightgreen", "test_video.mp4"),
            Video("Smartphone Displays Explained", "Technology", "0:10", "lightgreen", "smartphone_displays.mp4"),
            Video("Sample Video Demo", "Demo", "0:10", "lightgreen", "sample_video.mp4"),
            Video("Python Tutorial", "Education", "15:30", "lightgreen"),
            Video("Gaming Highlights", "Gaming", "8:45", "lightcoral"),
            Video("Cooking Basics", "Lifestyle", "12:20", "lightyellow"),
            Video("Tech Review", "Technology", "10:15", "lightblue"),
            Video("Music Video", "Entertainment", "3:45", "lightpink"),
            Video("News Update", "News", "5:30", "lightgray"),
            Video("Sports Highlights", "Sports", "7:20", "orange"),
            Video("Science Facts", "Education", "9:10", "lightcyan"),
        ]
        
        # TREE: Organize videos into category tree
        education_category = self.root_category.add_child_category("Education")
        entertainment_category = self.root_category.add_child_category("Entertainment")
        lifestyle_category = self.root_category.add_child_category("Lifestyle")
        tech_category = self.root_category.add_child_category("Technology")
        
        # Add programming subcategory under Education
        programming_category = education_category.add_child_category("Programming")
        
        # Distribute videos into categories
        for video in sample_videos:
            if video.category == "Education":
                if "Python" in video.title:
                    programming_category.add_video(video)
                else:
                    education_category.add_video(video)
            elif video.category in ["Gaming", "Music Video", "Entertainment"]:
                entertainment_category.add_video(video)
            elif video.category == "Lifestyle":
                lifestyle_category.add_video(video)
            elif video.category == "Technology":
                tech_category.add_video(video)
            else:
                self.root_category.add_video(video)
        
        # LINKED LIST: Add some videos to suggestions
        for video in sample_videos[:4]:
            self.suggestions.add_suggestion(video)
        
        # QUEUE: Add some videos to upload queue
        upload_videos = [
            Video("Pending Upload 1", "Education", "5:00", "yellow"),
            Video("Pending Upload 2", "Gaming", "8:30", "yellow"),
        ]
        for video in upload_videos:
            self.upload_queue.enqueue(video)
        
        # ARRAY/LIST: Create default playlists
        self.playlists["Favorites"] = Playlist("Favorites")
        self.playlists["Watch Later"] = Playlist("Watch Later")
        self.playlists["Educational"] = Playlist("Educational")
        self.playlists["Liked Videos"] = Playlist("Liked Videos")  # Auto-managed playlist for liked videos
        
        # Add some videos to playlists
        self.playlists["Educational"].add_video(sample_videos[1])  # Python Tutorial
        self.playlists["Educational"].add_video(sample_videos[8])  # Science Facts
        
        # Load any additional video files from workspace
        self.load_video_files_from_workspace()
    
    def load_video_files_from_workspace(self):
        """Automatically load video files found in the workspace"""
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        
        # Get current working directory
        workspace_dir = os.getcwd()
        
        try:
            for filename in os.listdir(workspace_dir):
                file_path = os.path.join(workspace_dir, filename)
                
                # Check if it's a video file
                if os.path.isfile(file_path):
                    name, ext = os.path.splitext(filename)
                    if ext.lower() in video_extensions:
                        # Create video object from file
                        video_title = name.replace('_', ' ').title()
                        duration = "Unknown"  # Could use video libraries to get real duration
                        
                        # Determine category based on filename keywords
                        category = "Videos"  # Default category
                        if any(keyword in name.lower() for keyword in ['tutorial', 'learn', 'education']):
                            category = "Education"
                        elif any(keyword in name.lower() for keyword in ['game', 'gaming', 'play']):
                            category = "Gaming"
                        elif any(keyword in name.lower() for keyword in ['music', 'song', 'audio']):
                            category = "Entertainment"
                        
                        # Create and add video
                        video = Video(video_title, category, duration, "lightsteelblue", file_path)
                        self.root_category.add_video(video)
                        
        except Exception as e:
            print(f"Error loading video files: {e}")
    
    def setup_ui(self):
        """Create the user interface"""
        # Create main frames
        self.create_frames()
        self.create_header()
        self.create_navigation_tabs()
        self.create_sidebar()
        self.create_main_content()
        self.create_now_playing_section()
        self.create_data_structure_panel()
        
        # Initialize theme
        self.is_dark_theme = True
    
    def create_frames(self):
        """Create main layout frames"""
        # Clean YouTube-style header
        self.header_frame = tk.Frame(self.root, bg="#0f0f0f", height=56)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Clean navigation tabs
        self.nav_tabs_frame = tk.Frame(self.root, bg="#0f0f0f", height=50)
        self.nav_tabs_frame.pack(fill=tk.X)
        self.nav_tabs_frame.pack_propagate(False)
        
        # Main content container
        self.content_container = tk.Frame(self.root, bg="#0f0f0f")
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Clean left sidebar
        self.sidebar_frame = tk.Frame(self.content_container, bg="#0f0f0f", width=240)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        # Main content area with clean background
        self.main_content_frame = tk.Frame(self.content_container, bg="#0f0f0f")
        self.main_content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel with minimal design
        self.right_panel = tk.Frame(self.content_container, bg="#0f0f0f", width=300)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
    def create_navigation_tabs(self):
        """Create clean YouTube-style navigation tabs"""
        # Clean tabs container  
        tabs_container = tk.Frame(self.nav_tabs_frame, bg="#0f0f0f")
        tabs_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=8)
        
        # Clean tab buttons
        tabs = [
            ("All", True),
            ("Music", False),
            ("Gaming", False),
            ("Live", False),
            ("Technology", False),
            ("Recently uploaded", False)
        ]
        
        self.tab_buttons = []
        for i, (tab_name, is_active) in enumerate(tabs):
            if is_active:
                btn = tk.Button(tabs_container, text=tab_name, 
                               font=("Segoe UI", 12, "bold"), bg="white", fg="#0f0f0f", 
                               relief=tk.FLAT, bd=0, padx=16, pady=8,
                               cursor="hand2", command=lambda t=tab_name: self.switch_tab(t))
            else:
                btn = tk.Button(tabs_container, text=tab_name, 
                               font=("Segoe UI", 12), bg="#272727", fg="#f1f1f1", 
                               relief=tk.FLAT, bd=0, padx=16, pady=8,
                               cursor="hand2", command=lambda t=tab_name: self.switch_tab(t),
                               activebackground="#373737")
            
            btn.pack(side=tk.LEFT, padx=6)
            self.tab_buttons.append(btn)
            
            # Clean hover effect
            if not is_active:
                self.add_hover_effect(btn, "#373737", "#272727")
    
    def switch_tab(self, tab_name):
        """Switch active tab and filter content"""
        # Reset all tabs to inactive state
        for btn in self.tab_buttons:
            btn.config(bg="#373737", fg="white", font=("Roboto", 11))
        
        # Set clicked tab as active
        for btn in self.tab_buttons:
            if btn.cget("text") == tab_name:
                btn.config(bg="white", fg="#0f0f0f", font=("Roboto", 11, "bold"))
                break
        
        # Filter videos based on tab
        if tab_name == "All":
            self.show_all_videos()
        else:
            # Filter videos by category/type
            filtered_videos = []
            all_videos = self.root_category.get_all_videos()
            
            for video in all_videos:
                if (tab_name.lower() in video.category.lower() or 
                    tab_name.lower() in video.title.lower()):
                    filtered_videos.append(video)
            
            self.content_title.config(text=f"{tab_name}")
            self.update_video_display(filtered_videos)
    
    def create_header(self):
        """Create clean YouTube-style header"""
        # Left section with menu and logo
        left_section = tk.Frame(self.header_frame, bg="#0f0f0f")
        left_section.pack(side=tk.LEFT, fill=tk.Y, padx=16)
        
        # Clean hamburger menu
        menu_btn = tk.Button(left_section, text="≡", font=("Segoe UI", 16), 
                           bg="#0f0f0f", fg="white", relief=tk.FLAT, bd=0,
                           padx=10, pady=12, cursor="hand2",
                           activebackground="#272727")
        menu_btn.pack(side=tk.LEFT, padx=(0, 24), pady=12)
        
        # Clean YouTube logo
        logo_frame = tk.Frame(left_section, bg="#0f0f0f")
        logo_frame.pack(side=tk.LEFT, pady=14)
        
        # YouTube icon
        play_button = tk.Label(logo_frame, text="▶", font=("Segoe UI", 12, "bold"), 
                             bg="#ff0000", fg="white", padx=4, pady=3,
                             relief=tk.FLAT)
        play_button.pack(side=tk.LEFT)
        
        title_label = tk.Label(logo_frame, text="YouTube", 
                              font=("Segoe UI", 18, "bold"), bg="#0f0f0f", fg="white")
        title_label.pack(side=tk.LEFT, padx=(6, 0))
        
        # Clean center search section
        center_section = tk.Frame(self.header_frame, bg="#0f0f0f")
        center_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=80)
        
        search_frame = tk.Frame(center_section, bg="#0f0f0f")
        search_frame.pack(expand=True, pady=12)
        
        # Clean search container
        search_container = tk.Frame(search_frame, bg="#202020", relief=tk.FLAT, bd=1)
        search_container.pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_container, width=50, font=("Segoe UI", 14), 
                                    bg="#202020", fg="white", insertbackground="white",
                                    relief=tk.FLAT, bd=0, highlightthickness=0)
        self.search_entry.pack(side=tk.LEFT, ipady=8, padx=16)
        self.search_entry.insert(0, "Search")
        self.search_entry.bind('<FocusIn>', self.clear_search_placeholder)
        self.search_entry.bind('<FocusOut>', self.restore_search_placeholder)
        
        # Clean search button
        search_btn = tk.Button(search_frame, text="🔍", font=("Segoe UI", 14), 
                              bg="#313131", fg="white", relief=tk.FLAT, bd=0,
                              padx=18, pady=9, command=self.search_videos,
                              cursor="hand2", activebackground="#404040")
        search_btn.pack(side=tk.LEFT, padx=(2, 12))
        
        # Clean voice search
        voice_btn = tk.Button(search_frame, text="🎤", font=("Segoe UI", 14), 
                             bg="#202020", fg="white", relief=tk.FLAT, bd=0,
                             padx=10, pady=8, cursor="hand2",
                             activebackground="#313131")
        voice_btn.pack(side=tk.LEFT)
        
        # Clean right section
        right_section = tk.Frame(self.header_frame, bg="#0f0f0f")
        right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=16)
        
        # Clean create button  
        create_btn = tk.Button(right_section, text="✚ Upload", 
                             font=("Segoe UI", 11), bg="#0f0f0f", fg="white", 
                             relief=tk.FLAT, bd=0, padx=12, pady=8,
                             cursor="hand2", command=self.show_upload_dialog,
                             activebackground="#272727")
        create_btn.pack(side=tk.LEFT, pady=14, padx=(0, 16))
        
        # Clean notifications
        notif_btn = tk.Button(right_section, text="🔔", font=("Segoe UI", 16), 
                             bg="#0f0f0f", fg="white", relief=tk.FLAT, bd=0,
                             padx=8, pady=8, cursor="hand2",
                             activebackground="#272727")
        notif_btn.pack(side=tk.LEFT, pady=14, padx=(0, 12))
        
        # Clean profile avatar
        profile_btn = tk.Button(right_section, text="YT", font=("Segoe UI", 12, "bold"), 
                               bg="#ff0000", fg="white", relief=tk.FLAT, bd=0,
                               width=3, height=1, cursor="hand2")
        profile_btn.pack(side=tk.LEFT, pady=14)
    
    def create_sidebar(self):
        """Create clean YouTube-style sidebar"""
        # Clean home section
        home_section = tk.Frame(self.sidebar_frame, bg="#0f0f0f")
        home_section.pack(fill=tk.X, padx=0, pady=(20, 0))
        
        self.create_nav_button(home_section, "🏠", "Home", lambda: self.show_all_videos(), active=True)
        self.create_nav_button(home_section, "▶️", "Shorts", lambda: self.show_shorts())
        self.create_nav_button(home_section, "📚", "Subscriptions", lambda: self.show_subscriptions())
        
        # Clean separator
        separator = tk.Frame(self.sidebar_frame, bg="#3a3a3a", height=1)
        separator.pack(fill=tk.X, padx=12, pady=12)
        
        # Clean "You" section
        you_section = tk.Frame(self.sidebar_frame, bg="#0f0f0f")
        you_section.pack(fill=tk.X, padx=0)
        
        # Clean section header
        you_header = tk.Label(self.sidebar_frame, text="You", 
                             font=("Segoe UI", 14, "bold"), bg="#0f0f0f", fg="white")
        you_header.pack(anchor="w", padx=12, pady=(0, 8))
        
        self.create_nav_button(you_section, "👤", "Your channel", lambda: self.show_channel())
        self.create_nav_button(you_section, "🕒", "History", lambda: self.show_history())
        self.create_nav_button(you_section, "📝", "Playlists", lambda: self.show_all_playlists())
        self.create_nav_button(you_section, "📺", "Your videos", lambda: self.show_your_videos())
        self.create_nav_button(you_section, "⏰", "Watch later", lambda: self.show_watch_later())
        self.create_nav_button(you_section, "👍", "Liked videos", lambda: self.show_liked_videos())
        
        # Another clean separator
        separator2 = tk.Frame(self.sidebar_frame, bg="#3a3a3a", height=1)
        separator2.pack(fill=tk.X, padx=12, pady=12)
        
        # Clean subscriptions section
        subs_label = tk.Label(self.sidebar_frame, text="Subscriptions", 
                             font=("Segoe UI", 14, "bold"), bg="#0f0f0f", fg="white")
        subs_label.pack(anchor="w", padx=12, pady=(0, 8))
        
        # Sample subscribed channels
        channels = [
            ("🎨", "Creative Channel"),
            ("🎮", "Gaming Pro"),
            ("📚", "Tech Reviews"),
            ("🎵", "Music Hub"),
        ]
        
        for icon, channel_name in channels:
            self.create_channel_button(self.sidebar_frame, icon, channel_name)
    
    def create_main_content(self):
        """Create clean main video content area"""
        # Clean content header
        content_header = tk.Frame(self.main_content_frame, bg="#0f0f0f")
        content_header.pack(fill=tk.X, padx=24, pady=(20, 12))
        
        self.content_title = tk.Label(content_header, text="Home", 
                                     font=("Segoe UI", 20, "bold"), bg="#0f0f0f", fg="white")
        self.content_title.pack(side=tk.LEFT)
        
        # Clean video grid container
        self.video_container = tk.Frame(self.main_content_frame, bg="#0f0f0f")
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=24)
        
        # Clean canvas for scrolling
        self.video_canvas = tk.Canvas(self.video_container, bg="#0f0f0f", highlightthickness=0)
        
        # Minimalist scrollbar
        scrollbar = tk.Scrollbar(self.video_container, orient="vertical", command=self.video_canvas.yview,
                                bg="#0f0f0f", troughcolor="#0f0f0f", activebackground="#555", width=12)
        
        self.video_grid_frame = tk.Frame(self.video_canvas, bg="#0f0f0f")
        
        # Bind mouse wheel to canvas
        self.video_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.video_grid_frame.bind(
            "<Configure>",
            lambda e: self.video_canvas.configure(scrollregion=self.video_canvas.bbox("all"))
        )
        
        self.video_canvas.create_window((0, 0), window=self.video_grid_frame, anchor="nw")
        self.video_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.video_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_now_playing_section(self):
        """Create minimal now playing section"""
        # Clean now playing bar
        self.now_playing_bar = tk.Frame(self.main_content_frame, bg="#1a1a1a", height=60)
        self.now_playing_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.now_playing_bar.pack_propagate(False)
        
        # Clean left section
        left_section = tk.Frame(self.now_playing_bar, bg="#1a1a1a")
        left_section.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        self.now_playing_label = tk.Label(left_section, text="Select a video to play", 
                                         font=("Segoe UI", 12), bg="#1a1a1a", fg="#ccc")
        self.now_playing_label.pack(pady=18)
        
        # Clean suggestions section
        right_section = tk.Frame(self.now_playing_bar, bg="#1a1a1a")
        right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        
        suggestions_frame = tk.Frame(right_section, bg="#1a1a1a")
        suggestions_frame.pack(pady=18)
        
        tk.Label(suggestions_frame, text="Up Next:", 
                font=("Segoe UI", 10), bg="#1a1a1a", fg="#888").pack(side=tk.LEFT, padx=(0, 8))
        
        self.suggestion_label = tk.Label(suggestions_frame, text="", 
                                        font=("Segoe UI", 10), bg="#1a1a1a", fg="white")
        self.suggestion_label.pack(side=tk.LEFT, padx=(0, 12))
        
        next_btn = tk.Button(suggestions_frame, text="Next", 
                           font=("Segoe UI", 9), bg="#272727", fg="white", 
                           relief=tk.FLAT, bd=0, padx=12, pady=4,
                           command=self.next_suggestion, activebackground="#333")
        next_btn.pack(side=tk.LEFT, padx=2)
    
    def create_data_structure_panel(self):
        """Create ultra-clean data structure panel"""
        # Clean panel header
        header_frame = tk.Frame(self.right_panel, bg="#0f0f0f")
        header_frame.pack(fill=tk.X, padx=16, pady=16)
        
        panel_title = tk.Label(header_frame, text="Activity", 
                              font=("Segoe UI", 16, "bold"), bg="#0f0f0f", fg="white")
        panel_title.pack(side=tk.LEFT)
        
        # Clean sections
        history_section = self.create_data_section("Watch History", "🕒")
        
        self.history_listbox = tk.Listbox(history_section, height=4, 
                                         bg="#1a1a1a", fg="white", 
                                         selectbackground="#333", font=("Segoe UI", 10),
                                         relief=tk.FLAT, bd=0, highlightthickness=0)
        self.history_listbox.pack(fill=tk.X, padx=16, pady=(0, 12))
        
        # Upload Queue
        queue_section = self.create_data_section("Upload Queue", "⬆️")
        
        self.queue_listbox = tk.Listbox(queue_section, height=3, 
                                       bg="#1a1a1a", fg="white", 
                                       selectbackground="#333", font=("Segoe UI", 10),
                                       relief=tk.FLAT, bd=0, highlightthickness=0)
        self.queue_listbox.pack(fill=tk.X, padx=16, pady=(0, 12))
        
        # Current Playlist
        playlist_section = self.create_data_section("Current Playlist", "📝")
        
        self.playlist_display_listbox = tk.Listbox(playlist_section, height=4, 
                                                  bg="#1a1a1a", fg="white", 
                                                  selectbackground="#333", font=("Segoe UI", 10),
                                                  relief=tk.FLAT, bd=0, highlightthickness=0)
        self.playlist_display_listbox.pack(fill=tk.X, padx=16, pady=(0, 12))
        
        # Clean statistics
        stats_section = self.create_data_section("Statistics", "📊")
        
        self.stats_frame = tk.Frame(stats_section, bg="#0f0f0f")
        self.stats_frame.pack(fill=tk.X, padx=16, pady=(0, 16))
    
    def update_displays(self):
        """Update all data structure displays"""
        # Only update displays that still exist
        self.update_video_display()
        self.update_history_display()
        self.update_queue_display()
        self.update_suggestion_display()
        self.update_stats_display()
    
    # Placeholder methods for removed UI elements
    def update_category_tree(self):
        """Placeholder - category tree removed"""
        pass
    
    def add_category_to_tree(self, parent, category):
        """Placeholder - category tree removed"""
        pass
    
    def update_playlist_buttons(self):
        """Placeholder - playlist buttons moved to sidebar"""
        pass
    
    def update_video_display(self, videos=None):
        """Update video display with ultra-clean grid layout"""
        # Clear existing videos
        for widget in self.video_grid_frame.winfo_children():
            widget.destroy()
        
        # Get videos to display
        if videos is None:
            videos = self.root_category.get_all_videos()
        
        # Configure clean grid (5 columns for cleaner look)
        columns = 4
        for i in range(columns):
            self.video_grid_frame.columnconfigure(i, weight=1, uniform="video_col")
        
        # Create clean video cards in grid
        row = 0
        col = 0
        for video in videos:
            self.create_video_card(video, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1
    
    def create_video_card(self, video, row, col):
        """Create ultra-clean YouTube-style video card"""
        # Main video card with clean design
        card_frame = tk.Frame(self.video_grid_frame, bg="#0f0f0f")
        card_frame.grid(row=row, column=col, padx=8, pady=12, sticky="nsew")
        
        # Clean video thumbnail
        thumbnail_frame = tk.Frame(card_frame, bg=video.thumbnail_color, 
                                  width=320, height=180, relief=tk.FLAT)
        thumbnail_frame.pack(fill=tk.X)
        thumbnail_frame.pack_propagate(False)
        
        # Minimal play overlay
        overlay_frame = tk.Frame(thumbnail_frame, bg=video.thumbnail_color)
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        play_overlay = tk.Label(overlay_frame, text="▶", 
                               font=("Segoe UI", 40), bg=video.thumbnail_color, 
                               fg="white", cursor="hand2")
        play_overlay.pack()
        play_overlay.bind("<Button-1>", lambda e, v=video: self.play_video(v))
        
        # Clean duration badge
        duration_label = tk.Label(thumbnail_frame, text=video.duration, 
                                 font=("Segoe UI", 9, "bold"), bg="#000000", fg="white",
                                 padx=4, pady=2)
        duration_label.place(relx=0.95, rely=0.95, anchor="se")
        
        # Clean video info section
        info_frame = tk.Frame(card_frame, bg="#0f0f0f")
        info_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Clean video title
        title_label = tk.Label(info_frame, text=video.title, 
                              font=("Segoe UI", 14, "bold"), bg="#0f0f0f", fg="white",
                              wraplength=280, justify="left", anchor="w")
        title_label.pack(fill=tk.X)
        
        # Video file indicator
        if video.file_path:
            if os.path.exists(video.file_path):
                file_indicator = tk.Label(info_frame, text="🎬 Video File Available", 
                                        font=("Segoe UI", 9), bg="#0f0f0f", fg="#00ff00")
            else:
                file_indicator = tk.Label(info_frame, text="❌ File Not Found", 
                                        font=("Segoe UI", 9), bg="#0f0f0f", fg="#ff4444")
            file_indicator.pack(anchor="w")
        
        # Clean metadata
        meta_frame = tk.Frame(info_frame, bg="#0f0f0f")
        meta_frame.pack(fill=tk.X, pady=(2, 0))
        
        channel_label = tk.Label(meta_frame, text="YouTube", 
                                font=("Segoe UI", 11), bg="#0f0f0f", fg="#aaa")
        channel_label.pack(anchor="w")
        
        stats_text = f"{video.views:,} views • {video.upload_date}"
        stats_label = tk.Label(meta_frame, text=stats_text, 
                              font=("Segoe UI", 11), bg="#0f0f0f", fg="#aaa")
        stats_label.pack(anchor="w")
        
        # Clean engagement stats
        engagement_frame = tk.Frame(info_frame, bg="#0f0f0f")
        engagement_frame.pack(fill=tk.X, pady=(1, 0))
        
        engagement_text = f"👍 {video.likes:,} • 💬 {len(video.comments)}"
        engagement_label = tk.Label(engagement_frame, text=engagement_text, 
                                   font=("Segoe UI", 10), bg="#0f0f0f", fg="#888")
        engagement_label.pack(anchor="w")
        
        # Clean action buttons
        action_frame = tk.Frame(info_frame, bg="#0f0f0f")
        action_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Clean play button
        play_btn = tk.Button(action_frame, text="▶ Play", 
                           font=("Segoe UI", 10, "bold"), bg="#ff0000", fg="white", 
                           relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                           command=lambda v=video: self.play_video(v))
        play_btn.pack(side=tk.LEFT, padx=(0, 4))
        
        # Clean like button
        like_color = "#065fd4" if video.user_reaction == 'like' else "#313131"
        like_btn = tk.Button(action_frame, text="👍", 
                           font=("Segoe UI", 10), bg=like_color, fg="white", 
                           relief=tk.FLAT, bd=0, padx=8, pady=6, cursor="hand2",
                           command=lambda v=video: self.toggle_like(v))
        like_btn.pack(side=tk.LEFT, padx=(0, 4))
        
        # Clean dislike button
        dislike_color = "#cc0000" if video.user_reaction == 'dislike' else "#313131"
        dislike_btn = tk.Button(action_frame, text="👎", 
                              font=("Segoe UI", 10), bg=dislike_color, fg="white", 
                              relief=tk.FLAT, bd=0, padx=8, pady=6, cursor="hand2",
                              command=lambda v=video: self.toggle_dislike(v))
        dislike_btn.pack(side=tk.LEFT, padx=(0, 4))
        
        # Clean comments button
        comment_btn = tk.Button(action_frame, text="💬", 
                              font=("Segoe UI", 10), bg="#313131", fg="white", 
                              relief=tk.FLAT, bd=0, padx=8, pady=6, cursor="hand2",
                              command=lambda v=video: self.show_comments(v))
        comment_btn.pack(side=tk.LEFT, padx=(0, 4))
        
        # Clean save button
        save_btn = tk.Button(action_frame, text="💾", 
                           font=("Segoe UI", 10), bg="#313131", fg="white", 
                           relief=tk.FLAT, bd=0, padx=8, pady=6, cursor="hand2",
                           command=lambda v=video: self.show_add_to_playlist(v))
        save_btn.pack(side=tk.LEFT)
        
        # Clean hover effects
        self.add_hover_effect(card_frame, "#1a1a1a", "#0f0f0f")
        self.add_hover_effect(play_btn, "#cc0000", "#ff0000")
    
    def update_history_display(self):
        """Update watch history display (Stack visualization)"""
        self.history_listbox.delete(0, tk.END)
        history = self.watch_history.get_all()
        
        for i, video in enumerate(history):
            prefix = "▶ " if i == 0 else "  "  # Show most recent with play icon
            self.history_listbox.insert(tk.END, f"{prefix}{video.title}")
        
        # Highlight most recent
        if history:
            self.history_listbox.selection_set(0)
    
    def update_queue_display(self):
        """Update upload queue display (Queue visualization)"""
        self.queue_listbox.delete(0, tk.END)
        queue_items = self.upload_queue.get_all()
        
        for i, video in enumerate(queue_items):
            prefix = "▶ " if i == 0 else "  "  # Show next to process with play icon
            self.queue_listbox.insert(tk.END, f"{prefix}{video.title}")
        
        # Highlight next to process
        if queue_items:
            self.queue_listbox.selection_set(0)
    
    # HELPER METHODS
    
    def create_nav_button(self, parent, icon, text, command, active=False):
        """Create clean navigation button for sidebar"""
        btn_frame = tk.Frame(parent, bg="#0f0f0f")
        btn_frame.pack(fill=tk.X, pady=1)
        
        if active:
            bg_color = "#272727"
            text_color = "white"
            font_weight = "bold"
        else:
            bg_color = "#0f0f0f"
            text_color = "#f1f1f1"
            font_weight = "normal"
        
        btn = tk.Button(btn_frame, text=f"{icon}  {text}", 
                       font=("Segoe UI", 12, font_weight), bg=bg_color, fg=text_color, 
                       relief=tk.FLAT, bd=0, anchor="w", padx=12, pady=12,
                       command=command, cursor="hand2",
                       activebackground="#272727")
        btn.pack(fill=tk.X)
        
        if not active:
            self.add_hover_effect(btn, "#1a1a1a", "#0f0f0f")
        
        return btn
    
    def create_data_section(self, title, icon):
        """Create clean data structure section"""
        section_frame = tk.Frame(self.right_panel, bg="#0f0f0f")
        section_frame.pack(fill=tk.X, pady=(0, 8))
        
        header = tk.Frame(section_frame, bg="#0f0f0f")
        header.pack(fill=tk.X, padx=16, pady=(8, 4))
        
        title_label = tk.Label(header, text=f"{icon} {title}", 
                              font=("Segoe UI", 12, "bold"), bg="#0f0f0f", fg="white")
        title_label.pack(anchor="w")
        
        return section_frame
    
    def add_hover_effect(self, widget, hover_color, normal_color):
        """Add hover effect to widgets"""
        def on_enter(event):
            widget.configure(bg=hover_color)
        
        def on_leave(event):
            widget.configure(bg=normal_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.video_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        # This would implement theme switching
        # For now, just show a message
        messagebox.showinfo("Theme", "Theme toggle coming soon!")
    
    def toggle_data_panel(self):
        """Toggle data structure panel visibility"""
        if self.right_panel.winfo_viewable():
            self.right_panel.pack_forget()
        else:
            self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
    
    def search_videos(self):
        """Search videos based on search entry"""
        query = self.search_entry.get().strip().lower()
        if not query:
            self.show_all_videos()
            return
        
        all_videos = self.root_category.get_all_videos()
        filtered_videos = [v for v in all_videos if query in v.title.lower() 
                          or query in v.category.lower()]
        
        self.content_title.config(text=f"Search: \"{self.search_entry.get()}\"")
        self.update_video_display(filtered_videos)
    
    def show_all_videos(self):
        """Show all videos"""
        self.content_title.config(text="Home")
        self.update_video_display()
    
    def show_library(self):
        """Show user's library"""
        self.content_title.config(text="Library")
        # Show playlists or saved videos
        all_playlist_videos = []
        for playlist in self.playlists.values():
            all_playlist_videos.extend(playlist.get_videos())
        self.update_video_display(all_playlist_videos)
    
    def show_history(self):
        """Show watch history"""
        self.content_title.config(text="Watch History")
        history_videos = self.watch_history.get_all()
        self.update_video_display(history_videos)
    
    def update_stats_display(self):
        """Update statistics display"""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Calculate stats
        all_videos = self.root_category.get_all_videos()
        total_videos = len(all_videos)
        total_playlists = len(self.playlists)
        history_count = len(self.watch_history.stack)
        queue_count = self.upload_queue.size()
        
        # Calculate engagement stats
        total_likes = sum(video.likes for video in all_videos)
        total_comments = sum(len(video.comments) for video in all_videos)
        liked_videos_count = sum(1 for video in all_videos if video.user_reaction == 'like')
        
        stats = [
            ("Total Videos", total_videos),
            ("Playlists", total_playlists),
            ("History Items", history_count),
            ("Queue Items", queue_count),
            ("Total Likes", f"{total_likes:,}"),
            ("Total Comments", f"{total_comments:,}"),
            ("Videos You Liked", liked_videos_count)
        ]
        
        for label, value in stats:
            stat_row = tk.Frame(self.stats_frame, bg="#181818")
            stat_row.pack(fill=tk.X, pady=2)
            
            tk.Label(stat_row, text=label, 
                    font=("Arial", 10), bg="#181818", fg="#aaaaaa").pack(side=tk.LEFT)
            
            tk.Label(stat_row, text=str(value), 
                    font=("Arial", 10, "bold"), bg="#181818", fg="white").pack(side=tk.RIGHT)
    
    # ====================
    # EVENT HANDLERS & VIDEO INTERACTIONS
    # ====================
    
    def on_category_select(self, event):
        """Handle category selection - placeholder since tree removed"""
        pass
    
    def toggle_like(self, video):
        """Toggle like status for a video"""
        video.toggle_like()
        
        # Auto-manage Liked Videos playlist
        liked_playlist = self.playlists.get("Liked Videos")
        if liked_playlist:
            if video.user_reaction == 'like':
                # Add to liked videos playlist
                liked_playlist.add_video(video)
            else:
                # Remove from liked videos playlist
                liked_playlist.remove_video(video)
        
        # Show feedback
        reaction_text = "Liked!" if video.user_reaction == 'like' else "Like removed"
        messagebox.showinfo("Like", f"{reaction_text} {video.title}")
        
        # Refresh the display to update button colors and counts
        self.update_video_display()
        self.update_stats_display()
    
    def toggle_dislike(self, video):
        """Toggle dislike status for a video"""
        video.toggle_dislike()
        
        # Show feedback
        reaction_text = "Disliked" if video.user_reaction == 'dislike' else "Dislike removed"
        messagebox.showinfo("Dislike", f"{reaction_text} - {video.title}")
        
        # Refresh the display to update button colors and counts
        self.update_video_display()
        self.update_stats_display()
    
    def show_comments(self, video):
        """Show ultra-clean comments window"""
        # Clean comments window
        comments_window = tk.Toplevel(self.root)
        comments_window.title(f"Comments - {video.title}")
        comments_window.geometry("600x500")
        comments_window.configure(bg="#0f0f0f")
        
        # Clean header
        header_frame = tk.Frame(comments_window, bg="#0f0f0f")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header_frame, text=video.title, 
                font=("Segoe UI", 16, "bold"), bg="#0f0f0f", fg="white").pack(anchor="w")
        
        stats_text = f"{len(video.comments)} comments • {video.likes:,} likes"
        tk.Label(header_frame, text=stats_text, 
                font=("Segoe UI", 12), bg="#0f0f0f", fg="#aaa").pack(anchor="w", pady=(4, 0))
        
        # Clean action buttons
        action_frame = tk.Frame(header_frame, bg="#0f0f0f")
        action_frame.pack(fill=tk.X, pady=(12, 0))
        
        like_color = "#065fd4" if video.user_reaction == 'like' else "#272727"
        like_btn = tk.Button(action_frame, text=f"👍 {video.likes:,}", 
                           font=("Segoe UI", 11), bg=like_color, fg="white", 
                           relief=tk.FLAT, bd=0, padx=16, pady=8, cursor="hand2",
                           command=lambda: self.toggle_like_in_comments(video, comments_window))
        like_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Separator
        separator = tk.Frame(comments_window, bg="#373737", height=1)
        separator.pack(fill=tk.X, padx=16)
        
        # New comment section
        new_comment_frame = tk.Frame(comments_window, bg="#181818")
        new_comment_frame.pack(fill=tk.X, padx=16, pady=16)
        
        tk.Label(new_comment_frame, text="Add a comment:", 
                font=("Arial", 12, "bold"), bg="#181818", fg="white").pack(anchor="w")
        
        # Comment input area
        input_frame = tk.Frame(new_comment_frame, bg="#181818")
        input_frame.pack(fill=tk.X, pady=(8, 0))
        
        comment_entry = tk.Text(input_frame, height=3, 
                              font=("Arial", 11), bg="#313131", fg="white", 
                              insertbackground="white", relief=tk.FLAT, 
                              wrap=tk.WORD)
        comment_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        button_frame = tk.Frame(input_frame, bg="#181818")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        submit_btn = tk.Button(button_frame, text="Comment", 
                             font=("Arial", 11, "bold"), bg="#4285f4", fg="white", 
                             relief=tk.FLAT, bd=0, padx=16, pady=8, cursor="hand2",
                             command=lambda: self.add_comment(video, comment_entry, comments_window))
        submit_btn.pack()
        
        # Comments display area with scrollbar
        comments_container = tk.Frame(comments_window, bg="#181818")
        comments_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        
        # Canvas and scrollbar for comments
        comments_canvas = tk.Canvas(comments_container, bg="#181818", highlightthickness=0)
        comments_scrollbar = tk.Scrollbar(comments_container, orient="vertical", command=comments_canvas.yview)
        comments_frame = tk.Frame(comments_canvas, bg="#181818")
        
        comments_frame.bind(
            "<Configure>",
            lambda e: comments_canvas.configure(scrollregion=comments_canvas.bbox("all"))
        )
        
        comments_canvas.create_window((0, 0), window=comments_frame, anchor="nw")
        comments_canvas.configure(yscrollcommand=comments_scrollbar.set)
        
        comments_canvas.pack(side="left", fill="both", expand=True)
        comments_scrollbar.pack(side="right", fill="y")
        
        # Display existing comments
        self.display_comments(video, comments_frame)
        
        # Bind mouse wheel to comments canvas
        def _on_mousewheel(event):
            comments_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        comments_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def toggle_like_in_comments(self, video, window):
        """Toggle like from within comments window"""
        video.toggle_like()
        
        # Auto-manage Liked Videos playlist
        liked_playlist = self.playlists.get("Liked Videos")
        if liked_playlist:
            if video.user_reaction == 'like':
                liked_playlist.add_video(video)
            else:
                liked_playlist.remove_video(video)
        
        window.destroy()  # Close and reopen to refresh
        self.show_comments(video)
        self.update_video_display()  # Update main display too
    
    def toggle_dislike_in_comments(self, video, window):
        """Toggle dislike from within comments window"""
        video.toggle_dislike()
        window.destroy()  # Close and reopen to refresh
        self.show_comments(video)
        self.update_video_display()  # Update main display too
    
    def add_comment(self, video, comment_entry, comments_window):
        """Add a new comment to the video"""
        comment_text = comment_entry.get("1.0", tk.END).strip()
        
        if not comment_text:
            messagebox.showwarning("Empty Comment", "Please enter a comment before submitting.")
            return
        
        # Add comment with current user (for demo, using "You")
        video.add_comment("You", comment_text)
        
        # Clear the input
        comment_entry.delete("1.0", tk.END)
        
        # Refresh comments display
        self.refresh_comments_display(video, comments_window)
        
        # Update main video display to show new comment count
        self.update_video_display()
        
        messagebox.showinfo("Comment Added", "Your comment has been added!")
    
    def refresh_comments_display(self, video, comments_window):
        """Refresh the comments display in the comments window"""
        comments_window.destroy()
        self.show_comments(video)
    
    def display_comments(self, video, comments_frame):
        """Display all comments for a video"""
        # Clear existing comments display
        for widget in comments_frame.winfo_children():
            widget.destroy()
        
        if not video.comments:
            no_comments_label = tk.Label(comments_frame, text="No comments yet. Be the first to comment!", 
                                        font=("Arial", 12), bg="#181818", fg="#aaaaaa")
            no_comments_label.pack(pady=20)
            return
        
        # Display each comment
        for i, comment in enumerate(video.comments):
            comment_container = tk.Frame(comments_frame, bg="#181818")
            comment_container.pack(fill=tk.X, pady=8, padx=8)
            
            # Comment header with username and timestamp
            header_frame = tk.Frame(comment_container, bg="#181818")
            header_frame.pack(fill=tk.X)
            
            username_label = tk.Label(header_frame, text=comment.username, 
                                     font=("Arial", 11, "bold"), bg="#181818", fg="#4285f4")
            username_label.pack(side=tk.LEFT)
            
            timestamp_label = tk.Label(header_frame, text=comment.timestamp, 
                                      font=("Arial", 10), bg="#181818", fg="#aaaaaa")
            timestamp_label.pack(side=tk.LEFT, padx=(8, 0))
            
            # Comment text
            text_label = tk.Label(comment_container, text=comment.text, 
                                font=("Arial", 11), bg="#181818", fg="white", 
                                wraplength=500, justify="left", anchor="w")
            text_label.pack(fill=tk.X, pady=(4, 0))
            
            # Comment actions
            actions_frame = tk.Frame(comment_container, bg="#181818")
            actions_frame.pack(fill=tk.X, pady=(4, 0))
            
            like_comment_btn = tk.Button(actions_frame, text=f"👍 {comment.likes}", 
                                       font=("Arial", 10), bg="#313131", fg="white", 
                                       relief=tk.FLAT, bd=0, padx=8, pady=2, cursor="hand2")
            like_comment_btn.pack(side=tk.LEFT, padx=(0, 8))
            
            reply_btn = tk.Button(actions_frame, text="Reply", 
                                font=("Arial", 10), bg="#313131", fg="white", 
                                relief=tk.FLAT, bd=0, padx=8, pady=2, cursor="hand2")
            reply_btn.pack(side=tk.LEFT)
            
            # Add hover effects
            self.add_hover_effect(like_comment_btn, "#404040", "#313131")
            self.add_hover_effect(reply_btn, "#404040", "#313131")
            
            # Separator line between comments
            if i < len(video.comments) - 1:
                separator = tk.Frame(comments_frame, bg="#373737", height=1)
                separator.pack(fill=tk.X, padx=16, pady=8)
    
    def find_category_by_name(self, category, name):
        """Find category by name in tree (tree traversal)"""
        if category.name == name:
            return category
        
        for child in category.children:
            result = self.find_category_by_name(child, name)
            if result:
                return result
        
        return None
    
    def play_video(self, video):
        """Play video (update now playing and add to history stack)"""
        self.current_video = video
        self.now_playing_label.config(text=f"▶ {video.title} ({video.duration})", fg="#00ff00")
        
        # STACK operation: Push video to watch history
        self.watch_history.push(video)
        self.update_history_display()
        self.update_stats_display()
        
        # Play video in embedded player
        if video.file_path and os.path.exists(video.file_path):
            self.open_video_player(video)
        else:
            messagebox.showinfo("Demo Mode", f"Demo: Playing {video.title}\n(No video file found at: {video.file_path})", parent=self.root)
    
    def show_add_to_playlist(self, video):
        """Show dialog to add video to playlist (Array/List operation)"""
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Add to Playlist")
        popup.geometry("300x200")
        popup.configure(bg="white")
        
        tk.Label(popup, text=f"Add '{video.title}' to:", 
                font=("Arial", 12), bg="white").pack(pady=10)
        
        # Playlist selection
        for name, playlist in self.playlists.items():
            btn = tk.Button(popup, text=f"{name} ({len(playlist.videos)} videos)", 
                           command=lambda p=playlist: self.add_to_playlist(video, p, popup),
                           bg="lightblue", width=25)
            btn.pack(pady=5)
        
        # Create new playlist option
        tk.Button(popup, text="Create New Playlist", 
                 command=lambda: self.create_new_playlist(video, popup),
                 bg="lightgreen", width=25).pack(pady=10)
    
    def add_to_playlist(self, video, playlist, popup):
        """Add video to playlist (Array/List operation)"""
        success = playlist.add_video(video)
        if success:
            messagebox.showinfo("Success", f"Added '{video.title}' to '{playlist.name}'")
            self.update_playlist_buttons()
            self.update_playlist_display_if_selected(playlist)
        else:
            messagebox.showwarning("Already Added", f"'{video.title}' is already in '{playlist.name}'")
        
        popup.destroy()
    
    def create_new_playlist(self, video, popup):
        """Create new playlist and add video"""
        popup.destroy()
        
        # Get playlist name
        name = tk.simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name:
            new_playlist = Playlist(name)
            new_playlist.add_video(video)
            self.playlists[name] = new_playlist
            
            self.update_playlist_buttons()
            messagebox.showinfo("Success", f"Created playlist '{name}' and added '{video.title}'")
    
    def show_upload_dialog(self):
        """Show video upload dialog"""
        from tkinter import filedialog, simpledialog
        
        # Choose to either select file or add to queue
        choice = messagebox.askyesnocancel(
            "Upload Video", 
            "Do you want to:\\n\\nYes = Select a video file from your computer\\nNo = Process pending uploads\\nCancel = Cancel",
            parent=self.root
        )
        
        if choice is True:  # Select file
            file_path = filedialog.askopenfilename(
                title="Select Video File",
                filetypes=[
                    ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                    ("All Files", "*.*")
                ],
                parent=self.root
            )
            
            if file_path:
                # Get video details
                filename = os.path.basename(file_path)
                default_title = os.path.splitext(filename)[0].replace('_', ' ').title()
                
                title = simpledialog.askstring("Video Title", "Enter video title:", initialvalue=default_title, parent=self.root)
                if not title:
                    return
                
                categories = ["Education", "Gaming", "Entertainment", "Technology", "Lifestyle", "Sports", "News", "Other"]
                category_popup = tk.Toplevel(self.root)
                category_popup.title("Select Category")
                category_popup.geometry("300x250")
                category_popup.configure(bg="#1a1a1a")
                category_popup.transient(self.root)
                category_popup.grab_set()
                
                selected_category = tk.StringVar(value="Other")
                
                tk.Label(category_popup, text="Select Category:", 
                        font=("Segoe UI", 12, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)
                
                for cat in categories:
                    rb = tk.Radiobutton(category_popup, text=cat, variable=selected_category, value=cat,
                                      font=("Segoe UI", 10), bg="#1a1a1a", fg="white", 
                                      selectcolor="#333333", activebackground="#333333")
                    rb.pack(anchor="w", padx=20)
                
                def confirm_upload():
                    # Create new video object
                    video = Video(title, selected_category.get(), self.get_video_duration(file_path), "lightsteelblue", file_path)
                    self.root_category.add_video(video)
                    self.update_displays()
                    
                    messagebox.showinfo("Upload Complete", f"Added video: {title}\\nFile: {filename}", parent=self.root)
                    category_popup.destroy()
                
                tk.Button(category_popup, text="Upload Video", command=confirm_upload,
                         font=("Segoe UI", 11, "bold"), bg="#ff0000", fg="white", 
                         relief=tk.FLAT, padx=20, pady=8, cursor="hand2").pack(pady=20)
                
        elif choice is False:  # Process queue
            self.process_upload_queue()
        
        # If choice is None (Cancel), do nothing
    
    def open_video_player(self, video):
        """Open embedded video player window"""
        # Create video player window
        player_window = tk.Toplevel(self.root)
        player_window.title(f"Playing: {video.title}")
        player_window.geometry("900x600")
        player_window.configure(bg="#000000")
        player_window.transient(self.root)
        
        # Video display area
        video_frame = tk.Frame(player_window, bg="#000000")
        video_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Video info header
        info_header = tk.Frame(video_frame, bg="#000000")
        info_header.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(info_header, text=video.title, 
                              font=("Segoe UI", 16, "bold"), bg="#000000", fg="white")
        title_label.pack(side=tk.LEFT)
        
        file_path_label = tk.Label(info_header, text=f"File: {os.path.basename(video.file_path)}", 
                                  font=("Segoe UI", 10), bg="#000000", fg="#888")
        file_path_label.pack(side=tk.RIGHT)
        
        # Placeholder for video display (black rectangle)\n        video_display = tk.Frame(video_frame, bg="#1a1a1a", height=400)\n        video_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))\n        \n        # Video placeholder content\n        placeholder_label = tk.Label(video_display, \n                                    text=f\"🎬\\n\\nVideo: {video.title}\\n\\nFile: {os.path.basename(video.file_path)}\\n\\nClick 'Play in System Player' to watch\", \n                                    font=(\"Segoe UI\", 14), bg=\"#1a1a1a\", fg=\"white\",\n                                    justify=tk.CENTER)\n        placeholder_label.place(relx=0.5, rely=0.5, anchor=\"center\")\n        \n        # Controls frame\n        controls_frame = tk.Frame(video_frame, bg=\"#000000\")\n        controls_frame.pack(fill=tk.X)\n        \n        # Control buttons\n        btn_frame = tk.Frame(controls_frame, bg=\"#000000\")\n        btn_frame.pack(pady=10)\n        \n        # Play in system player button\n        play_system_btn = tk.Button(btn_frame, text=\"▶ Play in System Player\", \n                                   font=(\"Segoe UI\", 12, \"bold\"), bg=\"#ff0000\", fg=\"white\", \n                                   relief=tk.FLAT, padx=20, pady=10, cursor=\"hand2\",\n                                   command=lambda: self.play_in_system_player(video.file_path))\n        play_system_btn.pack(side=tk.LEFT, padx=(0, 10))\n        \n        # Open folder button\n        folder_btn = tk.Button(btn_frame, text=\"📁 Open File Location\", \n                              font=(\"Segoe UI\", 11), bg=\"#333333\", fg=\"white\", \n                              relief=tk.FLAT, padx=20, pady=10, cursor=\"hand2\",\n                              command=lambda: self.open_file_location(video.file_path))\n        folder_btn.pack(side=tk.LEFT, padx=(0, 10))\n        \n        # Close button\n        close_btn = tk.Button(btn_frame, text=\"✕ Close Player\", \n                             font=(\"Segoe UI\", 11), bg=\"#666666\", fg=\"white\", \n                             relief=tk.FLAT, padx=20, pady=10, cursor=\"hand2\",\n                             command=player_window.destroy)\n        close_btn.pack(side=tk.LEFT)\n        \n        # Video info section\n        info_section = tk.Frame(controls_frame, bg=\"#000000\")\n        info_section.pack(fill=tk.X, pady=(10, 0))\n        \n        info_text = f\"Duration: {video.duration} | Views: {video.views:,} | Category: {video.category}\"\n        info_label = tk.Label(info_section, text=info_text, \n                             font=(\"Segoe UI\", 10), bg=\"#000000\", fg=\"#aaa\")\n        info_label.pack()\n        \n        # Center the window\n        player_window.update_idletasks()\n        x = (player_window.winfo_screenwidth() // 2) - (900 // 2)\n        y = (player_window.winfo_screenheight() // 2) - (600 // 2)\n        player_window.geometry(f\"900x600+{x}+{y}\")\n    \n    def play_in_system_player(self, file_path):\n        \"\"\"Play video in system's default player\"\"\"\n        try:\n            if platform.system() == \"Windows\":\n                os.startfile(file_path)\n            elif platform.system() == \"Darwin\":  # macOS\n                subprocess.call([\"open\", file_path])\n            else:  # Linux\n                subprocess.call([\"xdg-open\", file_path])\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not open video file: {e}\")\n    \n    def open_file_location(self, file_path):\n        \"\"\"Open file location in file explorer\"\"\"\n        try:\n            if platform.system() == \"Windows\":\n                subprocess.run([\"explorer\", \"/select,\", file_path])\n            elif platform.system() == \"Darwin\":  # macOS\n                subprocess.call([\"open\", \"-R\", file_path])\n            else:  # Linux\n                folder_path = os.path.dirname(file_path)\n                subprocess.call([\"xdg-open\", folder_path])\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not open file location: {e}\")
    
    def show_playlist(self, playlist):
        """Display playlist contents (Array/List visualization)"""
        self.content_title.config(text=f"Playlist: {playlist.name}")
        self.update_video_display(playlist.get_videos())
        
        # Update playlist display in right panel
        self.playlist_display_listbox.delete(0, tk.END)
        for i, video in enumerate(playlist.get_videos()):
            self.playlist_display_listbox.insert(tk.END, f"{i+1}. {video.title}")
    
    def update_playlist_display_if_selected(self, playlist):
        """Update playlist display if it's currently shown"""
        current_title = self.content_title.cget("text")
        if f"Playlist: {playlist.name}" in current_title:
            self.show_playlist(playlist)
    
    def process_upload_queue(self):
        """Process upload queue (Queue FIFO operation)"""
        if self.upload_queue.is_empty():
            messagebox.showinfo("Queue Empty", "No videos in upload queue")
            return
        
        # QUEUE operation: Dequeue (FIFO - First In, First Out)
        video = self.upload_queue.dequeue()
        
        # Add to main video collection
        self.root_category.add_video(video)
        
        messagebox.showinfo("Upload Processed", f"Processed upload: {video.title}")
        
        # Update displays
        self.update_displays()
    
    def next_suggestion(self):
        """Move to next suggestion (Linked List navigation)"""
        next_video = self.suggestions.next_suggestion()
        if next_video:
            self.update_suggestion_display()
        else:
            messagebox.showinfo("End of List", "No more suggestions available")
    
    def reset_suggestions(self):
        """Reset suggestions to beginning (Linked List reset)"""
        self.suggestions.reset()
        self.update_suggestion_display()
    
    def update_suggestion_display(self):
        """Update suggestion display (Linked List current item)"""
        current_suggestion = self.suggestions.get_current()
        if current_suggestion:
            self.suggestion_label.config(text=current_suggestion.title)
        else:
            self.suggestion_label.config(text="None")
    
    def update_stats_display(self):
        """Update statistics display"""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Calculate stats
        total_videos = len(self.root_category.get_all_videos())
        total_playlists = len(self.playlists)
        history_count = len(self.watch_history.stack)
        queue_count = self.upload_queue.size()
        
        stats = [
            ("Total Videos", total_videos),
            ("Playlists", total_playlists),
            ("History Items", history_count),
            ("Queue Items", queue_count)
        ]
        
        for label, value in stats:
            stat_row = tk.Frame(self.stats_frame, bg="#181818")
            stat_row.pack(fill=tk.X, pady=2)
            
            tk.Label(stat_row, text=label, 
                    font=("Arial", 10), bg="#181818", fg="#aaaaaa").pack(side=tk.LEFT)
            
            tk.Label(stat_row, text=str(value), 
                    font=("Arial", 10, "bold"), bg="#181818", fg="white").pack(side=tk.RIGHT)
    
    # New YouTube-style interface helper methods
    def create_navigation_tabs(self):
        """Create YouTube-style navigation tabs"""
        # Scrollable tabs container
        tabs_container = tk.Frame(self.nav_tabs_frame, bg="#212121")
        tabs_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=8)
        
        # Tab buttons with YouTube styling
        tabs = [
            ("All", True),  # Active tab
            ("Music", False),
            ("Mixes", False),
            ("Gaming", False),
            ("Live", False),
            ("Sports", False),
            ("News", False),
            ("Technology", False),
            ("Podcasts", False),
            ("Recently uploaded", False)
        ]
        
        self.tab_buttons = []
        for i, (tab_name, is_active) in enumerate(tabs):
            if is_active:
                btn = tk.Button(tabs_container, text=tab_name, 
                               font=("Roboto", 11, "bold"), bg="white", fg="#0f0f0f", 
                               relief=tk.FLAT, bd=0, padx=16, pady=6,
                               cursor="hand2", command=lambda t=tab_name: self.switch_tab(t))
            else:
                btn = tk.Button(tabs_container, text=tab_name, 
                               font=("Roboto", 11), bg="#373737", fg="white", 
                               relief=tk.FLAT, bd=0, padx=16, pady=6,
                               cursor="hand2", command=lambda t=tab_name: self.switch_tab(t))
            
            btn.pack(side=tk.LEFT, padx=4)
            self.tab_buttons.append(btn)
            
            # Add hover effect
            if not is_active:
                self.add_hover_effect(btn, "#464646", "#373737")
    
    def switch_tab(self, tab_name):
        """Switch active tab and filter content"""
        # Reset all tabs to inactive state
        for btn in self.tab_buttons:
            btn.config(bg="#373737", fg="white", font=("Roboto", 11))
        
        # Set clicked tab as active
        for btn in self.tab_buttons:
            if btn.cget("text") == tab_name:
                btn.config(bg="white", fg="#0f0f0f", font=("Roboto", 11, "bold"))
                break
        
        # Filter videos based on tab
        if tab_name == "All":
            self.show_all_videos()
        else:
            # Filter videos by category/type
            filtered_videos = []
            all_videos = self.root_category.get_all_videos()
            
            for video in all_videos:
                if (tab_name.lower() in video.category.lower() or 
                    tab_name.lower() in video.title.lower()):
                    filtered_videos.append(video)
            
            self.content_title.config(text=f"{tab_name}")
            self.update_video_display(filtered_videos)
    
    def clear_search_placeholder(self, event):
        """Clear search placeholder text"""
        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="white")
    
    def restore_search_placeholder(self, event):
        """Restore search placeholder if empty"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search")
            self.search_entry.config(fg="#aaaaaa")
    
    def create_channel_button(self, parent, icon, channel_name):
        """Create clean channel subscription button"""
        btn_frame = tk.Frame(parent, bg="#0f0f0f")
        btn_frame.pack(fill=tk.X, pady=1, padx=12)
        
        # Clean channel avatar
        avatar = tk.Label(btn_frame, text=icon, font=("Segoe UI", 12), 
                         bg="#ff0000", fg="white", width=3, height=1)
        avatar.pack(side=tk.LEFT, pady=6, padx=(0, 12))
        
        # Clean channel name
        name_label = tk.Label(btn_frame, text=channel_name, 
                             font=("Segoe UI", 11), bg="#0f0f0f", fg="white",
                             anchor="w")
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=6)
        
        # Clean hover effect
        btn_frame.bind("<Button-1>", lambda e: self.show_channel_videos(channel_name))
        avatar.bind("<Button-1>", lambda e: self.show_channel_videos(channel_name))
        name_label.bind("<Button-1>", lambda e: self.show_channel_videos(channel_name))
        
        self.add_hover_effect(btn_frame, "#1a1a1a", "#0f0f0f")
    
    # Placeholder methods for new sidebar functions
    def show_shorts(self):
        """Show shorts/short videos"""
        short_videos = [v for v in self.root_category.get_all_videos() if int(v.duration.split(':')[0]) < 5]
        self.content_title.config(text="Shorts")
        self.update_video_display(short_videos)
    
    def show_subscriptions(self):
        """Show subscription videos"""
        self.content_title.config(text="Subscriptions")
        self.update_video_display(self.root_category.get_all_videos()[:4])  # Recent uploads
    
    def show_channel(self):
        """Show user's channel"""
        self.content_title.config(text="Your Channel")
        messagebox.showinfo("Channel", "Your channel page would be shown here")
    
    def show_all_playlists(self):
        """Show all playlists overview"""
        self.content_title.config(text="Your Playlists")
        messagebox.showinfo("Playlists", f"You have {len(self.playlists)} playlists")
    
    def show_your_videos(self):
        """Show user's uploaded videos"""
        self.content_title.config(text="Your Videos")
        self.update_video_display(self.root_category.get_all_videos()[:2])  # Simulate user videos
    
    def show_watch_later(self):
        """Show watch later playlist"""
        if "Watch Later" in self.playlists:
            self.show_playlist(self.playlists["Watch Later"])
        else:
            self.content_title.config(text="Watch Later")
            self.update_video_display([])
    
    def show_liked_videos(self):
        """Show liked videos"""
        self.content_title.config(text="Liked Videos")
        
        # Filter videos that user has liked
        all_videos = self.root_category.get_all_videos()
        liked_videos = [video for video in all_videos if video.user_reaction == 'like']
        
        if liked_videos:
            self.update_video_display(liked_videos)
        else:
            # Show empty state if no liked videos
            self.update_video_display([])
            messagebox.showinfo("No Liked Videos", "You haven't liked any videos yet. Start exploring and like videos you enjoy!")
    
    def show_channel_videos(self, channel_name):
        """Show videos from a specific channel"""
        self.content_title.config(text=f"{channel_name}")
        # Show subset of videos for demo
        self.update_video_display(self.root_category.get_all_videos()[:3])
    
    def get_video_duration(self, file_path):
        """Get video duration using OpenCV"""
        try:
            cap = cv2.VideoCapture(file_path)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                duration_seconds = frame_count / fps if fps > 0 else 0
                cap.release()
                
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                return f"{minutes}:{seconds:02d}"
            else:
                return "Unknown"
        except:
            return "Unknown"

# ====================
# MAIN EXECUTION
# ====================

if __name__ == "__main__":
    # Import tkinter simpledialog for playlist creation
    import tkinter.simpledialog
    
    root = tk.Tk()
    app = MiniYouTubeApp(root)
    root.mainloop()