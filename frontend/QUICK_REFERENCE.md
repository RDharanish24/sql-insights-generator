# DataGenie Core - Quick Reference Guide

## 🚀 Quick Start

```bash
# Development
cd frontend
npm install
npm run dev

# Production Build
npm run build

# Preview
npm run preview
```

## 📊 Component Architecture

### Data Flow
```
Dashboard.jsx (State Management)
├── handles prompt state
├── manages loading/result/error states
├── fetches from http://localhost:8000/api/query
└── distributes to child components

App.jsx
└── Renders Dashboard
    ├── Header (Status display)
    ├── SearchController (Input)
    └── Main Content Area
        ├── IdleState (when no query)
        ├── LoadingState (during query)
        ├── ErrorState (on failure)
        └── Results (on success)
            ├── SqlTerminal
            ├── ChartRenderer
            └── DataTable
```

## 🎨 Styling Convention

### Class Naming Pattern
- **Glass Cards**: `glass-card`, `glass-card-strong`, `glass-card-highlight`
- **Animations**: `animate-fade-in-up`, `animate-fade-in-up-delay-1`, `animate-spin-slow`
- **Glows**: `glow-brand`, `glow-brand-strong`, `glow-emerald`
- **Text Styles**: `text-gradient-brand`

### Responsive Prefixes
- Mobile-first approach: no prefix = mobile
- `sm:` = 640px and up
- `md:` = 768px and up  
- `lg:` = 1024px and up
- `xl:` = 1280px and up

### Example
```jsx
<div className="text-base sm:text-lg md:text-xl lg:text-2xl">
  Responsive Text
</div>
```

## 🔑 Key Features Per Component

| Component | Features |
|-----------|----------|
| **Header** | Logo, status badges, connection indicator with pulse |
| **SearchController** | Glowing input, focus animations, button state changes |
| **IdleState** | 6 smart suggestions, hero icon, staggered animations |
| **LoadingState** | Spinner, progress indicators, skeleton loaders |
| **ErrorState** | Error message, retry button, helpful tips |
| **SqlTerminal** | Syntax highlighting, copy button, line numbers |
| **ChartRenderer** | 4 chart types, tooltips, responsive grid |
| **DataTable** | Pagination, export CSV, copy to clipboard |

## 🎯 State Management Pattern

```jsx
const [prompt, setPrompt] = useState('');
const [loading, setLoading] = useState(false);
const [result, setResult] = useState(null);
const [error, setError] = useState('');

// State determination logic
const isIdle = !loading && !result && !error;
const hasResults = !loading && result && !error;

// Render based on state
{isIdle && <IdleState />}
{loading && <LoadingState />}
{!loading && error && <ErrorState />}
{hasResults && <Results />}
```

## 🎨 Color Usage Guide

### For Accents
```jsx
// Primary - Indigo/Violet
className="text-brand-400" // #818cf8

// Secondary - Blue
className="text-accent-blue" // #3B82F6

// Success - Emerald
className="text-emerald-400" // #34d399

// Warning - Amber
className="text-amber-400" // #fbbf24

// Error - Rose
className="text-rose-400" // #fb7185

// Code - Cyan
className="text-cyan-300" // #22d3ee
```

### Background Layers
```jsx
// Dark base
className="bg-slate-950"

// Slightly lighter
className="bg-slate-900"

// Semi-transparent overlay
className="bg-slate-800/60"

// Glass effect
className="bg-slate-900/40 backdrop-blur-md"
```

## 🔄 Animation Classes

```jsx
// Fade in with upward motion
className="animate-fade-in-up"

// Delayed versions (use on sequential items)
className="animate-fade-in-up-delay-1"
className="animate-fade-in-up-delay-2"
className="animate-fade-in-up-delay-3"

// Slow spin (for loading)
className="animate-spin-slow"

// Pulse effect
className="animate-pulse"

// Float (for hero icons)
className="float-animation"
```

## 📐 Spacing System

```jsx
// Consistent spacing scale
px-4    // 16px horizontal
py-4    // 16px vertical
p-6     // 24px all sides
gap-3   // 12px between children
space-y-4 // 16px vertical between children
```

## 🔗 API Response Handling

```jsx
const response = await fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: query }),
});

// Success response structure
{
  "sql": "SELECT ... ",
  "data": [
    { "col1": "value1", "col2": 123 },
    ...
  ],
  "columns": ["col1", "col2"]
}

// Error response
{
  "detail": "Error message here"
}
```

## 🧪 Testing Interactive Elements

### Search Input
```jsx
// Focus state (shows glow)
input.focus()

// Type and submit
input.value = "test query"
form.submit()
```

### Copy Button
```jsx
// Check state change
button.click()
// Should show "Copied!" briefly then return to "Copy"
```

### Pagination
```jsx
// Navigate to next page
nextButton.click()

// Check pagination limit
if (page >= totalPages - 1) {
  nextButton.disabled === true
}
```

## 📱 Mobile Testing

### Breakpoints to Test
1. **375px** - iPhone SE
2. **430px** - Modern phones
3. **768px** - Tablets
4. **1024px** - Desktop
5. **1920px** - Large desktop

### Common Mobile Issues to Check
- [ ] Text doesn't overflow
- [ ] Buttons are large enough (min 44x44px)
- [ ] Horizontal scroll avoided
- [ ] Touch targets properly spaced
- [ ] Images responsive
- [ ] Navigation accessible

## 🔧 Customization Guide

### Change Primary Color
```css
/* In index.css @theme */
--color-brand-500: #YOUR_COLOR;
```

### Adjust Border Radius
```jsx
// Current: rounded-2xl (16px)
// Options: rounded-lg (8px), rounded-xl (12px), rounded-3xl (24px)
className="rounded-3xl"
```

### Modify Animation Speed
```jsx
// In CSS keyframes
animation: fade-in-up 0.5s ease-out both;
// Change 0.5s to your duration
```

### Disable Animations
```jsx
// Add to index.css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## 📦 Dependencies

```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "lucide-react": "^0.400.0",
  "recharts": "^2.12.7",
  "tailwindcss": "^4.0.0"
}
```

## 🐛 Debugging Tips

### Common Issues

**Issue**: Components not styling
- **Solution**: Check if `index.css` is imported in `main.jsx`

**Issue**: Icons not showing
- **Solution**: Ensure `lucide-react` is installed and imported correctly

**Issue**: Charts not rendering
- **Solution**: Verify data structure has at least one numeric column

**Issue**: Animations not smooth
- **Solution**: Check browser devtools performance, may need to reduce animation count

## 📖 Documentation Links

- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Lucide Icons](https://lucide.dev)
- [Recharts](https://recharts.org)

## 💡 Pro Tips

1. **Use `useMemo` for expensive calculations** (already done in ChartRenderer)
2. **Lazy load charts** if dealing with large datasets
3. **Debounce search input** to reduce API calls
4. **Cache API responses** to improve performance
5. **Use React DevTools** for component inspection
6. **Test with different viewport sizes** during development
7. **Monitor Lighthouse scores** for performance

## 🚨 Important Notes

- Ensure backend runs on `http://localhost:8000`
- Snowflake schema must be configured in backend
- Frontend expects specific response structure (see API Response Handling)
- All animations respect `prefers-reduced-motion`
- Tailwind builds from component classNames - no dynamic strings!

---

**Last Updated**: May 2026 | **Version**: 1.0
