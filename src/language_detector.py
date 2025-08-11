import os
from collections import Counter
from pathlib import Path
from typing import Optional, Dict, List


class LanguageDetector:
    """Detects programming language based on file extensions in current directory"""
    
    # Programming languages only (no config/markup files)
    LANGUAGE_PATTERNS = {
        'python': ['.py', '.pyx', '.pyi', '.pyw'],
        'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
        'typescript': ['.ts', '.tsx', '.d.ts'],
        'java': ['.java', '.class', '.jar'],
        'cpp': ['.cpp', '.cc', '.cxx', '.c++', '.hpp', '.h++', '.hxx'],
        'c': ['.c', '.h'],
        'csharp': ['.cs', '.csx'],
        'php': ['.php', '.phtml', '.php3', '.php4', '.php5'],
        'ruby': ['.rb', '.rbw', '.rake', '.gemspec'],
        'go': ['.go'],
        'rust': ['.rs', '.rlib'],
        'swift': ['.swift'],
        'kotlin': ['.kt', '.kts'],
        'scala': ['.scala', '.sc'],
        'dart': ['.dart'],
        'r': ['.r', '.R', '.rmd', '.Rmd'],
        'matlab': ['.m', '.mlx'],
        'shell': ['.sh', '.bash', '.zsh', '.fish'],
        'powershell': ['.ps1', '.psd1', '.psm1'],
        'flutter': ['.dart', 'pubspec.yaml', 'flutter.yaml'],
        'react': ['.jsx', '.tsx', 'package.json'],
        'vue': ['.vue'],
        'angular': ['.ts', 'angular.json', 'ng.json'],
        'node': ['.js', 'package.json', 'package-lock.json'],
        'django': ['.py', 'manage.py', 'settings.py'],
        'flask': ['.py', 'app.py', 'wsgi.py'],
        'laravel': ['.php', 'artisan', 'composer.json'],
        'rails': ['.rb', 'Gemfile', 'config.ru'],
        'spring': ['.java', 'pom.xml', 'build.gradle']
    }
    
    # Framework/technology specific files
    FRAMEWORK_INDICATORS = {
        'flutter': ['pubspec.yaml', 'lib/', 'android/', 'ios/'],
        'react': ['package.json', 'src/', 'public/', 'node_modules/'],
        'vue': ['package.json', 'vue.config.js', 'src/'],
        'angular': ['angular.json', 'src/', 'package.json'],
        'django': ['manage.py', 'settings.py', 'urls.py'],
        'flask': ['app.py', 'wsgi.py', 'requirements.txt'],
        'laravel': ['artisan', 'composer.json', 'app/', 'routes/'],
        'rails': ['Gemfile', 'config.ru', 'app/', 'config/'],
        'spring': ['pom.xml', 'src/main/java/', 'application.properties'],
        'node': ['package.json', 'node_modules/', 'index.js']
    }
    
    
    def __init__(self, directory: str = None):
        self.directory = Path(directory) if directory else Path.cwd()
    
    def detect_language(self) -> Optional[str]:
        """Detect the primary programming language in the directory"""
        if not self.directory.exists():
            return None
        
        # First check for framework indicators
        framework = self._detect_framework()
        if framework:
            return framework
        
        # Count file extensions
        extension_counts = self._count_extensions()
        if not extension_counts:
            return None
        
        # Find the most likely language
        language_scores = {}
        
        for language, extensions in self.LANGUAGE_PATTERNS.items():
            score = 0
            for ext in extensions:
                if ext in extension_counts:
                    score += extension_counts[ext]
            if score > 0:
                language_scores[language] = score
        
        if not language_scores:
            return None
        
        # Return the language with the highest score
        return max(language_scores.items(), key=lambda x: x[1])[0]
    
    def _detect_framework(self) -> Optional[str]:
        """Detect specific frameworks or technologies (non-recursive)"""
        for framework, indicators in self.FRAMEWORK_INDICATORS.items():
            matches = 0
            for indicator in indicators:
                if indicator.endswith('/'):
                    # Directory indicator - only check direct subdirectories
                    dir_name = indicator.rstrip('/')
                    if (self.directory / dir_name).is_dir():
                        matches += 1
                else:
                    # File indicator - only check current directory
                    if (self.directory / indicator).exists():
                        matches += 1
            
            # If we find at least 2 indicators, it's likely this framework
            if matches >= 2:
                return framework
        
        return None
    
    def _count_extensions(self) -> Dict[str, int]:
        """Count file extensions in the directory (non-recursive)"""
        extension_counts = Counter()
        
        try:
            # Only scan current directory, not subdirectories
            for item in self.directory.iterdir():
                if item.is_file():
                    # Skip hidden files and common non-code files
                    if item.name.startswith('.') and item.name not in ['Dockerfile', '.dockerfile']:
                        continue
                    
                    # Handle special cases
                    if item.name.lower() in ['dockerfile', 'makefile', 'gemfile', 'rakefile']:
                        extension_counts[item.name.lower()] += 1
                    elif item.suffix:
                        extension_counts[item.suffix.lower()] += 1
                        
            # Also check common subdirectories for framework detection (limited depth)
            common_dirs = ['src', 'lib', 'app', 'components', 'pages', 'views', 'controllers']
            for dir_name in common_dirs:
                subdir = self.directory / dir_name
                if subdir.is_dir():
                    try:
                        # Only count a few files from each common directory
                        file_count = 0
                        for item in subdir.iterdir():
                            if item.is_file() and file_count < 10:  # Limit to 10 files per subdir
                                if not item.name.startswith('.') and item.suffix:
                                    extension_counts[item.suffix.lower()] += 1
                                    file_count += 1
                    except PermissionError:
                        continue
                        
        except PermissionError:
            pass
        
        return dict(extension_counts)
    
    def get_language_context(self) -> str:
        """Get context string about detected language for AI prompts"""
        language = self.detect_language()
        if not language:
            return ""
        
        context_map = {
            'python': "Python project",
            'javascript': "JavaScript project", 
            'typescript': "TypeScript project",
            'java': "Java project",
            'cpp': "C++ project",
            'c': "C project",
            'csharp': "C# project",
            'php': "PHP project",
            'ruby': "Ruby project",
            'go': "Go project",
            'rust': "Rust project",
            'swift': "Swift project",
            'kotlin': "Kotlin project",
            'dart': "Dart project",
            'flutter': "Flutter mobile app",
            'react': "React.js web application",
            'vue': "Vue.js application", 
            'angular': "Angular application",
            'django': "Django web application",
            'flask': "Flask web application",
            'laravel': "Laravel web application",
            'rails': "Ruby on Rails application",
            'spring': "Spring Boot application",
            'node': "Node.js application"
        }
        
        return context_map.get(language, f"{language} project")