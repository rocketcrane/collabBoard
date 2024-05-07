// types.ts

export interface Sticky {
    x: number; // X coordinate
    y: number; // Y coordinate
    w: number; // Width
    h: number; // Height
    isTheme: boolean; // Whether it's a theme
    text: string; // Content text
  }
  
  export interface Concept {
    // title: string; // Concept title
    details: string; // Concept details
  }
  
  export interface GeneratedImage {
    image_prompt: string; // Description of the image prompt
    url: string; // URL to the generated image
  }
  
  export interface Summary {
    title: string; // Summary title
    details: string; // Summary details
  }
  
  export interface JSONData {
    stickies: Sticky[]; // List of sticky notes
    generated_concepts: Concept[]; // List of concepts
    generated_images: GeneratedImage[]; // Generated image data
    generated_summary: Summary[]; // Summary of the project
  }
  