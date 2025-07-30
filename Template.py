class jisshu_template(object):
    """
    Clean and professional template configuration for Jisshu video player
    Focused on user experience with minimal distractions
    """
    
    JISSHU_NAME = "Jisshu"

    JISSHU_DISCLAIMER = (
        "This service helps you stream videos online without downloading. "
        "We respect content creators and encourage reporting any copyright issues, "
        "inappropriate content, or violations through our support channel."
    )

    JISSHU_REPORT_LINK = "https://t.me/Jisshu_support"

    # Clean, professional color scheme
    # Removed excessive gradients and flashy colors for better UX
    JISSHU_COLOURS = {
        "primary": {
            "background": "#2563eb",  # Professional blue
            "color": "#ffffff"
        },
        "secondary": {
            "background": "#64748b",  # Neutral gray
            "color": "#ffffff"
        },
        "success": {
            "background": "#059669",  # Clean green
            "color": "#ffffff"
        },
        "warning": {
            "background": "#d97706",  # Subtle orange
            "color": "#ffffff"
        },
        "danger": {
            "background": "#dc2626",  # Clean red
            "color": "#ffffff"
        },
        "header": {
            "background": "#ffffff",  # Clean white header
            "color": "#0f172a",       # Dark text
            "border": "#e2e8f0"       # Light border
        },
        "background": {
            "light": "#f8fafc",       # Light mode background
            "dark": "#0f172a"         # Dark mode background
        },
        "text": {
            "primary": "#0f172a",     # Primary text color
            "secondary": "#475569",   # Secondary text color
            "muted": "#64748b"        # Muted text color
        },
        "border": {
            "light": "#e2e8f0",       # Light mode borders
            "dark": "#334155"         # Dark mode borders
        }
    }

    # Player button configurations (simplified)
    PLAYER_BUTTONS = {
        "mx_player": {
            "label": "MX Player",
            "icon": "fas fa-play",
            "class": "btn-primary"
        },
        "vlc_player": {
            "label": "VLC Player", 
            "icon": "fab fa-vlc",
            "class": "btn-success"
        },
        "playit_player": {
            "label": "PlayIt Player",
            "icon": "fas fa-play-circle", 
            "class": "btn-warning"
        },
        "download": {
            "label": "Download",
            "icon": "fas fa-download",
            "class": "btn-danger"
        }
    }

    # Feature flags for clean interface
    FEATURES = {
        "show_animations": False,        # Disabled flashy animations
        "show_gradients": False,         # Disabled gradient backgrounds
        "minimal_mode": True,            # Enable minimal clean mode
        "professional_theme": True,      # Enable professional styling
        "keyboard_shortcuts": True,      # Enable keyboard controls
        "skip_controls": True,          # Enable 10s forward/backward
        "theme_toggle": True,           # Enable dark/light theme
        "loading_spinner": True,        # Show loading states
        "notifications": True           # Show user feedback
    }

    # Typography settings for clean look
    TYPOGRAPHY = {
        "font_family": "'Inter', sans-serif",
        "font_weights": {
            "light": 300,
            "normal": 400, 
            "medium": 500,
            "semibold": 600
        },
        "font_sizes": {
            "small": "0.875rem",
            "normal": "1rem",
            "large": "1.125rem",
            "xl": "1.25rem"
        }
    }

    # Layout settings for better UX
    LAYOUT = {
        "max_width": "1200px",
        "container_padding": "1rem",
        "border_radius": {
            "small": "6px",
            "medium": "8px", 
            "large": "12px"
        },
        "shadows": {
            "small": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
            "medium": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            "large": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
        }
    }

    @classmethod
    def get_clean_config(cls):
        """
        Returns the complete clean configuration
        """
        return {
            "name": cls.JISSHU_NAME,
            "disclaimer": cls.JISSHU_DISCLAIMER,
            "report_link": cls.JISSHU_REPORT_LINK,
            "colors": cls.JISSHU_COLOURS,
            "buttons": cls.PLAYER_BUTTONS,
            "features": cls.FEATURES,
            "typography": cls.TYPOGRAPHY,
            "layout": cls.LAYOUT
        }

    @classmethod 
    def is_minimal_mode(cls):
        """Check if minimal mode is enabled"""
        return cls.FEATURES.get("minimal_mode", True)

    @classmethod
    def supports_keyboard_shortcuts(cls):
        """Check if keyboard shortcuts are enabled"""
        return cls.FEATURES.get("keyboard_shortcuts", True)

    @classmethod
    def has_skip_controls(cls):
        """Check if skip controls are enabled"""
        return cls.FEATURES.get("skip_controls", True)
