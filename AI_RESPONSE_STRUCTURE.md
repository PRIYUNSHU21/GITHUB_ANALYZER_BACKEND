# 🤖 AI Response Structure Documentation

## Overview
This document shows the exact structure of AI responses from the Enhanced GitHub Repository Analyzer API.

## Live API Base URL
```
https://github-analyzer-backend-g300.onrender.com
```

## Main Analysis Endpoint
```
POST /api/v1/analyze
Content-Type: application/json
{
  "owner": "facebook",
  "repo": "react"
}
```

## Complete Response Structure

### 📊 Full Response Example (facebook/react)
```json
{
  "owner": "facebook",
  "repo": "react",
  
  "stats": {
    "stars": 238595,
    "forks": 49248,
    "open_issues": 1037,
    "license": "MIT License"
  },
  
  "languages": {
    "languages": {
      "JavaScript": 67.41,
      "TypeScript": 29.07,
      "HTML": 1.5,
      "CSS": 1.06,
      "C++": 0.58,
      "CoffeeScript": 0.24,
      "C": 0.07,
      "Shell": 0.06,
      "Python": 0.0,
      "Makefile": 0.0
    }
  },
  
  "commit_activity": {
    "total_commits": 1485,
    "last_30_days": 100,
    "weekly_data": [
      {"week": "2024-09-08", "commits": 37},
      {"week": "2024-09-15", "commits": 36},
      {"week": "2024-09-22", "commits": 33},
      // ... 49 more weeks (52 total)
      {"week": "2025-08-31", "commits": 6}
    ]
  },
  
  "contributors": {
    "total_contributors": 100,
    "active_contributors": 100,
    "top_contributors": [
      {
        "username": "sebmarkbage",
        "commits": 1810,
        "avatar_url": "https://avatars.githubusercontent.com/u/63648?v=4"
      },
      {
        "username": "zpao",
        "commits": 1778,
        "avatar_url": "https://avatars.githubusercontent.com/u/8445?v=4"
      },
      {
        "username": "gaearon",
        "commits": 1680,
        "avatar_url": "https://avatars.githubusercontent.com/u/810438?v=4"
      },
      {
        "username": "acdlite",
        "commits": 1416,
        "avatar_url": "https://avatars.githubusercontent.com/u/3624098?v=4"
      },
      {
        "username": "sophiebits",
        "commits": 1290,
        "avatar_url": "https://avatars.githubusercontent.com/u/6820?v=4"
      }
    ]
  },
  
  "links": {
    "repo_url": "https://github.com/facebook/react",
    "owner_url": "https://github.com/facebook"
  },
  
  "ai_insights": {
    "repository_summary": {
      "content": "This GitHub repository contains the source code for React, a popular JavaScript library for building user interfaces. Its core purpose is to simplify the creation of interactive and dynamic web and native applications through a component-based and declarative programming model. Key features include declarative rendering, reusable components, and efficient updates.",
      "generated_at": "2025-09-03T13:39:34.232809"
    },
    "language_analysis": {
      "content": "The repository primarily uses JavaScript and TypeScript, indicating a focus on front-end development with a preference for type safety. The lack of a prominent back-end language suggests it's not a full-stack framework like MERN or MEAN, but rather a front-end library possibly targeting both web and native (likely via technologies like React Native or similar). The small percentage of other languages like C++ might suggest the inclusion of performance-critical components or native modules.",
      "generated_at": "2025-09-03T13:39:34.232819"
    },
    "contribution_patterns": {
      "content": "The project exhibits extremely high collaboration, with nearly all contributors actively engaged. The dominance of three top contributors, however, suggests a core team leads development, despite the large number of participants. Consistent contributions over a long period (from 2013 to 2025) indicate a healthy, actively maintained project.",
      "generated_at": "2025-09-03T13:39:34.232821"
    }
  }
}
```

## 🎯 AI Insights Breakdown

### 1. Repository Summary
- **Purpose**: General overview of what the repository does
- **Content**: Description of the project, its main purpose, and key features
- **Example**: "This GitHub repository contains the source code for React, a popular JavaScript library..."

### 2. Language Analysis  
- **Purpose**: Technical analysis of the programming languages used
- **Content**: Insights about technology stack, architectural decisions, and technical focus
- **Example**: "The repository primarily uses JavaScript and TypeScript, indicating a focus on front-end development..."

### 3. Contribution Patterns
- **Purpose**: Analysis of collaboration and development patterns
- **Content**: Insights about team structure, activity levels, and project health
- **Example**: "The project exhibits extremely high collaboration, with nearly all contributors actively engaged..."

## 📈 Data Structures

### Weekly Commit Data
```json
{
  "week": "2025-08-31",     // ISO date (YYYY-MM-DD)
  "commits": 6              // Number of commits that week
}
```

### Contributor Data
```json
{
  "username": "sebmarkbage",
  "commits": 1810,
  "avatar_url": "https://avatars.githubusercontent.com/u/63648?v=4"
}
```

### Language Data
```json
{
  "JavaScript": 67.41,     // Percentage of codebase
  "TypeScript": 29.07,
  "HTML": 1.5
}
```

## 🔧 Individual Endpoints

### Health Check
```
GET /api/v1/health
Response: {
  "status": "healthy",
  "ai_available": true
}
```

### Basic Stats
```
GET /api/v1/repo/{owner}/{repo}/stats
Response: {
  "stars": 238595,
  "forks": 49248,
  "open_issues": 1037,
  "license": "MIT License",
  "created_at": "2013-05-24T16:15:54Z"
}
```

### Contributors
```
GET /api/v1/repo/{owner}/{repo}/contributors
Response: {
  "total_contributors": 100,
  "active_contributors": 100,
  "top_contributors": [...]
}
```

### Commit Activity
```
GET /api/v1/repo/{owner}/{repo}/commits/activity
Response: {
  "total_commits": 1485,
  "last_30_days": 100,
  "weekly_data": [...]
}
```

## 🎨 Frontend Integration Tips

### For Flutter Development:

#### 1. Data Models
```dart
class AIInsight {
  final String content;
  final DateTime generatedAt;
  
  AIInsight({required this.content, required this.generatedAt});
  
  factory AIInsight.fromJson(Map<String, dynamic> json) {
    return AIInsight(
      content: json['content'],
      generatedAt: DateTime.parse(json['generated_at']),
    );
  }
}

class WeeklyCommitData {
  final String week;
  final int commits;
  
  WeeklyCommitData({required this.week, required this.commits});
  
  factory WeeklyCommitData.fromJson(Map<String, dynamic> json) {
    return WeeklyCommitData(
      week: json['week'],
      commits: json['commits'],
    );
  }
}
```

#### 2. Chart Data Preparation
```dart
// For fl_chart LineChart
List<FlSpot> getCommitChartData(List<WeeklyCommitData> weeklyData) {
  return weeklyData.asMap().entries.map((entry) {
    return FlSpot(entry.key.toDouble(), entry.value.commits.toDouble());
  }).toList();
}

// For fl_chart PieChart  
List<PieChartSectionData> getLanguageChartData(Map<String, double> languages) {
  final colors = [Colors.blue, Colors.red, Colors.green, Colors.orange, Colors.purple];
  
  return languages.entries.take(5).toList().asMap().entries.map((entry) {
    return PieChartSectionData(
      value: entry.value.value,
      title: '${entry.value.key}\n${entry.value.value.toStringAsFixed(1)}%',
      color: colors[entry.key % colors.length],
      radius: 100,
    );
  }).toList();
}
```

#### 3. AI Insights Display
```dart
class AIInsightCard extends StatelessWidget {
  final String title;
  final AIInsight insight;
  final IconData icon;
  
  const AIInsightCard({
    Key? key,
    required this.title,
    required this.insight,
    required this.icon,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Theme.of(context).primaryColor),
                const SizedBox(width: 8),
                Text(title, style: Theme.of(context).textTheme.titleMedium),
              ],
            ),
            const SizedBox(height: 12),
            Text(insight.content),
            const SizedBox(height: 8),
            Text(
              'Generated: ${insight.generatedAt.toString()}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
```

## ✅ Verified Response Fields

All these fields are tested and working in production:

- ✅ **Stats**: stars, forks, open_issues, license
- ✅ **Languages**: Dictionary with percentages (up to 10 languages)
- ✅ **Commit Activity**: total_commits, last_30_days, weekly_data (52 weeks)
- ✅ **Contributors**: total_contributors, active_contributors, top_contributors (5 users)
- ✅ **AI Insights**: All 3 types with content and timestamps
- ✅ **Links**: repo_url, owner_url

## 🚀 Ready for Frontend Implementation!

The backend API is fully functional and provides all the data structures needed for your Flutter frontend. All AI insights are generated in real-time and provide meaningful analysis of the repositories.

Use the test files generated (`test_response_*.json`) as reference examples for your frontend development!
