# MTG Card Creator Application - Rebuild Prompt

## Overview

This prompt can be used to recreate the Magic: the Gathering Card Creator web application from scratch.

---

## Prompt

**IMPORTANT: First invoke the `branding` skill to apply professional design standards, then proceed with implementation.**

Create a locally running web application on port 8080 using Node.js that allows users to create custom Magic: the Gathering cards with the following specifications:

### Technical Stack

- Node.js with Express web server
- Canvas API (node-canvas) for server-side image generation
- HTML/CSS/JavaScript frontend
- No database required

### Features Required

#### 1. Web Form with all MTG card fields

- **Card Name**
- **Mana Cost** (support for W, U, B, R, G, and colorless mana symbols)
- **Card Type** (dropdown: Creature, Instant, Sorcery, Enchantment, Artifact, Planeswalker, Land)
- **Subtype**
- **Rarity** (dropdown: Common, Uncommon, Rare, Mythic Rare)
- **Card Rules Text**
- **Flavor Text**
- **Power/Toughness** (show only for creatures)
- **Artist Name**

#### 2. Dynamic Artwork Generation

Auto-generate card artwork based on card properties:

**Mana-based color gradients:**
- Single color: gradient in that mana's color
- Multi-color: blend all colors together
- Colorless: gray gradient

**Type-specific decorative patterns:**
- Creatures: claw marks
- Instants/Sorceries: magical circles and stars
- Artifacts: geometric gear patterns
- Enchantments: flowing waves
- Other: diamond grid

**Visual presentation:**
- Display card name artistically in the center of artwork area

#### 3. Card Image Generation

- Generate a complete MTG card layout using Canvas
- Standard card dimensions (745x1040 pixels)
- Proper card frame with borders
- Render mana symbols as colored circles with letters
- Text wrapping for card text and flavor text
- Power/Toughness box for creatures
- Return as downloadable PNG image

#### 4. Professional Branding & Styling

**Use the branding skill for all visual design standards:**
- Apply brand color palette from branding skill for primary colors, accents, and backgrounds
- Use branding skill typography standards (Arial for headings, Calibri for body text)
- Follow branding skill color usage guidelines for buttons, inputs, and UI elements

**Modern, professional UI with:**
- Two-column layout (form on left, preview on right)
- Responsive design
- Smooth hover effects and transitions
- Brand-compliant color scheme throughout

#### 5. User Experience

- Real-time card preview
- Download button to save card as PNG
- Loading states during generation
- Console logging for debugging
- Automatic mana cost formatting
- Hide/show power/toughness based on card type

### Deliverables

- Complete working application
- All files organized (server.js, public/index.html, public/styles.css, public/script.js)
- Server running on http://localhost:8080
- Instructions for testing

---

## Example Test Card

**Lightning Dragon:**

- Card Name: Lightning Dragon
- Mana Cost: 3RR
- Card Type: Creature
- Subtype: Dragon
- Rarity: Rare
- Card Text / Rules: Flying, Haste. When Lightning Dragon enters the battlefield, it deals 3 damage to any target.
- Flavor Text: "Its roar shakes the mountains and splits the sky."
- Power: 5
- Toughness: 4
- Artist: Your Name

**Expected Result:**
- Red gradient background in artwork area
- Creature-specific claw mark patterns
- "Lightning Dragon" displayed prominently in center
- Complete, downloadable MTG card

---

## Color Reference

### Mana Colors for Gradients
*(Use these for MTG-specific card artwork generation)*

- **W (White)**: #f9faf4 - Light cream
- **U (Blue)**: #0e68ab - Ocean blue
- **B (Black)**: #150b00 - Deep black/brown
- **R (Red)**: #d3202a - Crimson red
- **G (Green)**: #00733e - Forest green
- **Colorless**: Gray gradient (#4a4a4a to #2a2a2a)

### UI Brand Colors
*(These are applied via the branding skill - reference only)*

- Dark Navy: #1F497D (Dark 2 from brand guidelines)
- Accent Blue: #4F81BD (Accent 1 from brand guidelines)
- Gold/Amber: #BF9000 (Frequently used color from brand guidelines)
- Accent Green: #9BBB59 (Accent 3 from brand guidelines)
- Light Cream: #EEECE1 (Light 2 from brand guidelines)
- White: #FFFFFF (Light 1 from brand guidelines)
- Black: #000000 (Dark 1 from brand guidelines)
- Medium Gray: #666666 (Secondary text from brand guidelines)

---

## Implementation Steps

1. **Invoke the branding skill** to load brand guidelines
2. **Set up the Node.js project** and install dependencies
3. **Apply brand colors and typography** from the branding skill to all UI elements
4. **Build the form and card generation logic**
5. **Test with example cards**

## Technical Notes

### Dependencies

```bash
npm install express canvas
```

### Server Structure

- Express server listening on port 8080
- Middleware for JSON and URL-encoded bodies
- Static file serving from 'public' directory
- POST endpoint `/generate-card` for card generation

### Canvas Rendering

- Use node-canvas for server-side rendering
- Card dimensions: 745x1040 pixels
- Art area: 665x480 pixels (positioned at 40, 80)
- Implement helper functions for:
  - Drawing card frame
  - Rendering mana symbols
  - Text wrapping
  - Pattern generation
  - Color manipulation (lighten/darken)

### Frontend

- FormData collection from HTML form
- Fetch API for card generation request
- Blob handling for image display and download
- Event listeners for form submission and download

---

## File Structure

```
project-directory/
├── server.js
├── package.json
└── public/
    ├── index.html
    ├── styles.css
    └── script.js
```

---

*Generated: 2025-12-01*
*Application: MTG Card Creator v1.0*
