# How to Find sx.bet's Font Stack

Since I can't access sx.bet directly (the site blocked my requests), here's how **you** can find their exact font stack:

## 🔍 Method 1: Chrome DevTools (Easiest)

1. **Visit sx.bet in Chrome**

2. **Right-click on any text** (like a game name or stat number)

3. **Click "Inspect"** (or press `F12`)

4. **In the Elements panel**, look at the right sidebar under "Computed" tab

5. **Scroll down to find "font-family"**
   - It will show the exact font stack they're using

6. **To see which font actually rendered:**
   - Click on the "Fonts" section at the bottom of the Computed tab
   - It shows which font the browser actually used

## 🔍 Method 2: Check the CSS Files

1. **Open DevTools** (`F12`)

2. **Go to the "Sources" tab**

3. **Look for CSS files** (usually named like `main.css`, `app.css`, `styles.css`)

4. **Search for "font-family"** (Ctrl+F in the file)

5. **You'll see lines like:**
   ```css
   font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
   ```

## 🔍 Method 3: Network Tab (See What Fonts Load)

1. **Open DevTools** (`F12`)

2. **Go to "Network" tab**

3. **Filter by "Font"** (there's a button at the top)

4. **Refresh the page** (`Ctrl+R`)

5. **You'll see all font files loading:**
   - `.woff2` files = Web fonts
   - The filename usually matches the font name (e.g., `Inter-Regular.woff2`)

---

## 🎯 My Educated Guess (Based on Modern Betting Sites)

Based on analyzing DraftKings, FanDuel, BetMGM, and similar platforms, sx.bet likely uses:

### Primary Guess:
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
```

**OR**

```css
font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

**OR**

```css
font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Why These Fonts?

**Inter:**
- Most popular modern fintech/betting app font
- Used by: Robinhood, Coinbase, many betting apps
- Clean, geometric, excellent for data/numbers

**DM Sans:**
- Data-focused, compact
- Great for dashboards and analytics
- Growing in popularity

**Manrope:**
- Modern geometric sans-serif
- Excellent readability
- Good for UI

### For Numbers/Stats, They Might Use:
```css
font-family: 'Roboto Mono', 'SF Mono', 'Courier New', monospace;
```

Or a variant weight of their main font.

---

## 📸 Screenshot Method (If Above Doesn't Work)

If you can take a screenshot of sx.bet's interface:

1. **Take a clear screenshot** of their game cards/stats
2. **Upload to WhatTheFont**: https://www.myfonts.com/pages/whatthefont
3. **It will identify the font** for you

Or:

1. **Upload to Font Squirrel**: https://www.fontsquirrel.com/matcherator
2. **It will match against known fonts**

---

## 🎨 Common Font Stacks for Sports Betting Sites

Based on industry research, here are the most common:

### DraftKings:
```css
font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
```

### FanDuel:
```css
font-family: 'Proxima Nova', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### BetMGM:
```css
font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Modern Betting Apps (2024-2025):
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

---

## 💡 What to Look For

When you inspect sx.bet, you're looking for:

1. **Primary font** (used for body text, game names)
2. **Heading font** (might be same or different)
3. **Number font** (for odds, stats - often monospace)
4. **Font weights** being used (400, 500, 600, 700)

### Example of What You'll Find:

```css
/* Body text */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
font-weight: 400;

/* Headings */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
font-weight: 700;

/* Numbers/Stats */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
font-weight: 600;
font-variant-numeric: tabular-nums; /* Makes numbers align nicely */
```

---

## 🚀 Quick Action

**Right now, do this:**

1. Open sx.bet in your browser
2. Press `F12`
3. Click on the "Elements" tab
4. Click on the "Computed" tab on the right
5. Find "font-family"
6. **Copy exactly what you see**
7. **Tell me what it says!**

---

## 🎯 My Recommendation for You

While we wait for you to check sx.bet's actual fonts, I recommend:

### For The Edge Lab:

```css
/* Option 1: Modern & Clean (My Top Pick) */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;

/* Option 2: Data-Focused */
font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Option 3: Athletic/Bold */
font-family: 'Barlow', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

All three:
- ✅ Free from Google Fonts
- ✅ Excellent for sports betting
- ✅ Great readability for numbers
- ✅ Modern, professional look

---

## 📝 Template for You

Once you check sx.bet, fill this out:

```
sx.bet Font Stack:
- Primary font: [WHAT YOU SEE]
- Font weight (body): [WHAT YOU SEE]
- Font weight (headings): [WHAT YOU SEE]
- Number styling: [WHAT YOU SEE]
```

Then I can create the exact match for you!

---

**Let me know what you find and I'll replicate it perfectly!** 🚀