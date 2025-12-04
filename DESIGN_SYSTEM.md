# MajayjayScholars Design System

## Design Philosophy
Clean, modern, and professional interface with a white base and purple gradient accents. Emphasis on readability, accessibility, and smooth interactions.

---

## Color Palette

### Primary Colors
- **Primary Gradient**: Linear gradient from #667eea (Soft Purple) to #764ba2 (Deep Purple) at 135deg
- **Primary Purple**: #667eea
- **Deep Purple**: #764ba2

### Neutral Colors
- **Background**: #f7fafc (Light Gray-Blue)
- **Surface/Cards**: #ffffff (Pure White)
- **Text Primary**: #2d3748 (Dark Gray)
- **Text Secondary**: #4a5568 (Medium Gray)
- **Text Tertiary**: #718096 (Light Gray)
- **Text Muted**: #a0aec0 (Very Light Gray)

### Border & Divider Colors
- **Border Light**: #e2e8f0
- **Border Medium**: #cbd5e0
- **Divider**: #e0e0e0

### State Colors
- **Hover Background**: rgba(102, 126, 234, 0.1)
- **Focus Ring**: rgba(102, 126, 234, 0.1)
- **Active State**: Linear gradient #667eea to #764ba2

### Semantic Colors
- **Success**: #48bb78 (Green)
- **Success Light**: #d4edda
- **Success Dark**: #155724
- **Error**: #f56565 (Red)
- **Error Light**: #f8d7da
- **Error Dark**: #721c24
- **Info**: #667eea (Primary Purple)

---

## Typography

### Font Family
- **Primary**: 'Inter', sans-serif
- **Fallback**: System fonts (sans-serif)

### Font Sizes
- **Heading 1**: 28px (1.75rem)
- **Heading 2**: 24px (1.5rem)
- **Heading 3**: 22px (1.375rem)
- **Body Large**: 16px (1rem)
- **Body**: 14px (0.875rem)
- **Small**: 12px (0.75rem)

### Font Weights
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

### Line Heights
- **Tight**: 1.2
- **Normal**: 1.5
- **Relaxed**: 1.75

---

## Spacing System
Based on 4px grid system:
- **xs**: 4px
- **sm**: 8px
- **md**: 12px
- **base**: 16px
- **lg**: 20px
- **xl**: 24px
- **2xl**: 32px
- **3xl**: 40px
- **4xl**: 48px

---

## Border Radius
- **Small**: 8px
- **Medium**: 10px
- **Large**: 12px
- **XLarge**: 16px
- **2XLarge**: 24px
- **Circle**: 50%

---

## Shadows

### Elevation Levels
- **Level 1**: 0 2px 10px rgba(0,0,0,0.05)
- **Level 2**: 0 4px 20px rgba(0,0,0,0.08)
- **Level 3**: 0 6px 20px rgba(102, 126, 234, 0.4)
- **Level 4**: 0 8px 30px rgba(102, 126, 234, 0.15)

### Component Shadows
- **Card**: 0 4px 20px rgba(0,0,0,0.08)
- **Button Hover**: 0 6px 20px rgba(102, 126, 234, 0.4)
- **Sidebar**: 0 4px 20px rgba(0,0,0,0.08)
- **Navbar**: 0 2px 10px rgba(0,0,0,0.05)

---

## Components

### Buttons

#### Primary Button
- **Background**: Linear gradient 135deg from #667eea to #764ba2
- **Text Color**: #ffffff
- **Padding**: 12px 20px (vertical, horizontal)
- **Border Radius**: 12px
- **Font Weight**: 600
- **Shadow**: 0 4px 15px rgba(102, 126, 234, 0.3)
- **Hover**: Transform translateY(-2px), shadow 0 6px 20px rgba(102, 126, 234, 0.4)
- **Transition**: all 0.3s ease

#### Secondary Button
- **Background**: rgba(102, 126, 234, 0.1)
- **Text Color**: #667eea
- **Padding**: 12px 20px
- **Border Radius**: 10px
- **Font Weight**: 500
- **Hover**: Background rgba(102, 126, 234, 0.2)

### Input Fields
- **Background**: #f7fafc
- **Border**: 2px solid #e2e8f0
- **Border Radius**: 10px
- **Padding**: 12px 16px
- **Font Size**: 14px
- **Focus State**: 
  - Border color: #667eea
  - Background: #ffffff
  - Box shadow: 0 0 0 3px rgba(102, 126, 234, 0.1)

### Cards
- **Background**: #ffffff
- **Border**: 1px solid #e2e8f0
- **Border Radius**: 16px
- **Padding**: 32px
- **Shadow**: 0 4px 20px rgba(0,0,0,0.08)
- **Hover**: Transform translateY(-5px), shadow 0 8px 30px rgba(102, 126, 234, 0.15)

### Sidebar
- **Width**: 250px
- **Background**: #ffffff
- **Border Right**: 1px solid #e2e8f0
- **Shadow**: 0 4px 20px rgba(0,0,0,0.08)
- **Padding**: 20px

#### Sidebar Links
- **Default**: 
  - Color: #2d3748
  - Padding: 12px 15px
  - Border radius: 12px
  - Font weight: 500
- **Hover**: 
  - Background: rgba(102, 126, 234, 0.1)
  - Color: #667eea
  - Transform: translateX(5px)
- **Active**: 
  - Background: Linear gradient #667eea to #764ba2
  - Color: #ffffff
  - Shadow: 0 4px 15px rgba(102, 126, 234, 0.3)

#### Sidebar Title
- **Background**: Linear gradient text from #667eea to #764ba2
- **Font Size**: 22px
- **Font Weight**: 600
- **Text Align**: center

### Navbar/Topbar
- **Background**: #ffffff
- **Border Bottom**: 1px solid #e2e8f0
- **Shadow**: 0 2px 10px rgba(0,0,0,0.05)
- **Padding**: 20px 30px
- **Height**: 80px

### Tables
- **Header Background**: #f8f9fa
- **Header Text**: #333333
- **Header Font Weight**: 600
- **Border**: 2px solid #e0e0e0 (header), 1px solid #e0e0e0 (rows)
- **Row Hover**: Background #f8f9fa
- **Cell Padding**: 15px

### Badges
- **Background**: Linear gradient #667eea to #764ba2
- **Color**: #ffffff
- **Padding**: 5px 12px
- **Border Radius**: 12px
- **Font Size**: 12px
- **Font Weight**: 600

### Stat Cards
- **Background**: #ffffff
- **Border**: 1px solid #e2e8f0
- **Border Radius**: 16px
- **Padding**: 25px
- **Shadow**: 0 4px 20px rgba(0,0,0,0.08)
- **Number Color**: #667eea
- **Number Size**: 36px
- **Number Weight**: 700
- **Label Color**: #666666
- **Label Size**: 14px
- **Hover**: Transform translateY(-5px), border color #667eea

---

## Animations & Transitions

### Standard Transitions
- **Duration**: 0.3s
- **Easing**: ease

### Hover Effects
- **Buttons**: translateY(-2px)
- **Cards**: translateY(-5px)
- **Sidebar Links**: translateX(5px)

### Focus States
- **Ring**: 0 0 0 3px rgba(102, 126, 234, 0.1)

---

## Layout

### Sidebar Layout
- **Sidebar Width**: 250px (fixed)
- **Main Content Margin**: 250px left
- **Sidebar Hidden**: -260px left
- **Content Expanded**: 0px margin

### Responsive Breakpoints
- **Mobile**: max-width 768px
  - Sidebar: Hidden by default (left: -260px)
  - Main content: margin-left 0
  - Sidebar toggle: Shows sidebar when active

### Grid System
- **Stats Grid**: repeat(auto-fit, minmax(200px, 1fr))
- **Gap**: 20px

---

## Icons & Imagery

### Logo
- **Size**: 80px × 80px
- **Border Radius**: 50% (circle)
- **Object Fit**: contain
- **Margin**: 0 auto 15px

### Icon Style
- **Type**: Emoji-based icons
- **Size**: Inline with text
- **Examples**: 🏠 🏛 👥 📄 📁 📝 🔄

---

## Form Elements

### Labels
- **Color**: #4a5568
- **Font Size**: 14px
- **Font Weight**: 500
- **Margin Bottom**: 8px

### Input States
- **Default**: Background #f7fafc, border #e2e8f0
- **Focus**: Background #ffffff, border #667eea
- **Disabled**: Background #edf2f7, opacity 0.6, cursor not-allowed
- **Read-only**: Background #edf2f7

### File Inputs
- **Margin Bottom**: 20px
- **Helper Text**: Color #718096, size 12px

---

## Authentication Pages (Login/Register)

### Layout
- **Container**: Max-width 1000-1100px
- **Background**: #f7fafc
- **Card**: White with shadow
- **Split Design**: 
  - Left: Gradient purple sidebar with logo
  - Right: White form area

### Gradient Sidebar
- **Background**: Linear gradient #667eea to #764ba2
- **Logo Border**: 4px solid rgba(255, 255, 255, 0.3)
- **Logo Shadow**: 0 10px 30px rgba(0, 0, 0, 0.2)
- **Text Color**: #ffffff
- **Text Shadow**: 0 2px 10px rgba(0, 0, 0, 0.2)

---

## Accessibility

### Contrast Ratios
- **Text on White**: Minimum 4.5:1
- **Primary Purple on White**: Passes WCAG AA
- **White on Purple Gradient**: Passes WCAG AAA

### Focus Indicators
- **Visible**: 3px ring with 0.1 opacity
- **Color**: Primary purple (#667eea)

### Interactive Elements
- **Minimum Touch Target**: 44px × 44px
- **Hover States**: Always visible
- **Active States**: Clear visual feedback

---

## Mobile Design Prompt

**For Mobile App Implementation:**

Create a mobile application with a clean, modern design using a white base (#f7fafc) with purple gradient accents (linear gradient from #667eea to #764ba2 at 135 degrees). 

**Key Design Elements:**
1. Use Inter font family throughout
2. Primary actions use the purple gradient with white text
3. Cards are white with subtle shadows (0 4px 20px rgba(0,0,0,0.08))
4. Input fields have light gray backgrounds (#f7fafc) with 2px borders (#e2e8f0)
5. Focus states show purple borders with a subtle ring effect
6. All interactive elements have smooth 0.3s transitions
7. Buttons lift slightly on press (translateY effect)
8. Use 12px border radius for buttons and inputs, 16px for cards
9. Spacing follows 4px grid system (8px, 12px, 16px, 20px, 24px)
10. Text colors: primary #2d3748, secondary #4a5568, muted #718096
11. Success states use green (#48bb78), errors use red (#f56565)
12. Navigation uses bottom tab bar or drawer with same purple gradient for active states
13. Headers can use gradient text effect (purple gradient with text clipping)
14. Maintain consistent 16-20px padding on screen edges
15. Use elevation/shadows sparingly for depth hierarchy

**Color Palette:**
- Primary: #667eea to #764ba2 gradient
- Background: #f7fafc
- Surface: #ffffff
- Text: #2d3748, #4a5568, #718096
- Borders: #e2e8f0
- Success: #48bb78
- Error: #f56565

**Typography:**
- Headings: 22-28px, weight 600-700
- Body: 14-16px, weight 400-500
- Small: 12px, weight 400

**Spacing:**
- Tight: 8px
- Normal: 16px
- Loose: 24px
- Section: 32-40px
