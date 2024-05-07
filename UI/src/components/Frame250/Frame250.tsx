import { memo } from 'react';
import type { FC } from 'react';
import React, { useState, useEffect } from 'react';

import resets from '../_resets.module.css';
import { Ellipse107Icon } from './Ellipse107Icon.js';
import classes from './Frame250.module.css';

import { JSONData, Sticky, Concept, GeneratedImage } from '../../types';


interface Props {
  className?: string;
  data: JSONData;
  
}


/* @figmaId 65:2276 */
export const Frame250: FC<Props> = memo(function Frame250({ data, className }: Props) {
  const { generated_concepts, generated_summary, generated_images } = data;

  const generatedImages = data.generated_images;

  // Get the URL of the first image (assuming there's at least one image)
  const imageUrl = generatedImages.length > 0 ? generatedImages[0].url : '';
  // Get the URL of the second image (assuming there are at least two images)
  const imageUrl2 = generatedImages.length > 1 ? generatedImages[1].url : '';

  // Create a dynamic CSS class with inline styles
  const dynamicCssClass = `
    .rectangle74 {
      position: absolute;
      left: 1055px;
      top: 660px;
      width: 418px;
      height: 418px;
      border-radius: 18px;
      background-image: url(${imageUrl});
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;
    }
  `;

    // Create a dynamic CSS class with inline styles
    const dynamicCssClass2 = `
    .rectangle80 {
      position: absolute;
      right: 0px;
      top: 660px;
      width: 418px;
      height: 418px;
      border-radius: 18px;
      background-image: url(${imageUrl2});
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;
    }
  `;

  // Inject the dynamic CSS class into the head of the document
  const styleElement = document.createElement('style');
  styleElement.innerHTML = dynamicCssClass;
  document.head.appendChild(styleElement);

  // Inject the dynamic CSS class2 into the head of the document
  const styleElement2 = document.createElement('style');
  styleElement2.innerHTML = dynamicCssClass2;
  document.head.appendChild(styleElement2); 

  // // Remap stickies' coordinates to the bottom left quarter of the canvas
  // const remappedStickies = data.stickies.map((sticky: Sticky) => ({
  //   ...sticky,
  //   x: sticky.x < 520 ? sticky.x : sticky.x - 520, // Remap x coordinate
  //   y: sticky.y > -166 ? sticky.y + 166 : sticky.y,// Remap y coordinate
  // }));

  // Define scale factor and translation values
  const scaleFactor = 0.5; // Scale down by half
  const translateX = 0; // No horizontal translation
  const translateY = 950 * scaleFactor; // Translate to the bottom of the canvas

  // Remap stickies' coordinates to the bottom left quarter of the canvas
  const remappedStickies = data.stickies.map((sticky: Sticky) => ({
    ...sticky,
    x: sticky.x * scaleFactor + translateX,
    y: sticky.y * scaleFactor + translateY,
  }));

  // Filter stickies that are not themes
  const notThemeStickies = remappedStickies.filter(sticky => !sticky.isTheme);
  

  return (
    <div className={`${resets.clapyResets} ${classes.root}`}>
      <div className={classes.rectangle72}></div>
      {/* <div className={classes.rectangle74}></div> Generated Images */}
      <div className={`rectangle74`}>
      </div>

      {/* <div className={classes.rectangle80}></div> Generated Images */}
      <div className={`rectangle80`}>
      </div>
      <div className={classes.rectangle79}></div>
      <div className={classes.titleOfTheConcent}>
        {/* Title of the content */}
        {data.stickies.find(sticky => sticky.isTheme)?.text}
      </div>
      <div className={classes.rectangle73}></div>
      <div className={classes.line59}></div>
      <div className={classes.line60}></div>
      {/* <div className={classes.rectangle75}></div>
      <div className={classes.rectangle76}></div>
      <div className={classes.rectangle77}></div>
      <div className={classes.rectangle78}></div> */}
      

    <div className="sticky-container">
      {notThemeStickies.map((sticky: Sticky, index: number) => (
        <React.Fragment key={`${index}-${sticky.x}-${sticky.y}`}> {/* Composite key */}
          {/* Box */}
          <div
            className={`sticky-box ${sticky.isTheme ? 'theme' : 'nottheme'}`}
            style={{
              position: 'absolute',
              left: `${sticky.x}px`, // Adjusted left position
              top: `${sticky.y}px`, // Adjusted top position
              width: `${sticky.w}px`,
              height: `${sticky.h}px`,
              border: '1px solid black', // Add border for visibility
            }}
          ></div>

          {/* Label */}
          <div
            className="sticky-label"
            style={{
              position: 'absolute',
              left: `${sticky.x}px`,
              top: `${sticky.y + sticky.h + 5}px`, // Adjusted top position to be below the box
              // transform: 'translateX(-50%)',
            }}
          >
            {sticky.text}
          </div>
        </React.Fragment>
      ))}
    </div>

      <div className={classes.ellipse107}>
        <Ellipse107Icon className={classes.icon} />
      </div>
      <div className={classes.rectangle732}></div>
      {/* <div className={classes.loremIpsumIsSimplyDummy}>Lorem Ipsum is simply dummy</div> */}
      {/* <div className={classes.concept01}>
            <div>
              <h4>{generated_concepts[0].title}</h4>
            </div>
      </div> */}

      <div className={classes.concept01Detail}>
        <div>
          <p>{generated_concepts[0].details}</p>
        </div>
      </div>

      
      <div className={classes.rectangle82}></div>
      {/* <div className={classes.loremIpsumIsSimplyDummy2}>Lorem Ipsum is simply dummy</div> */}
      {/* <div className={classes.concept02}>
        <div>
          <h4>{generated_concepts[1].title}</h4>
        </div>
      </div> */}

      <div className={classes.concept02Detail}>
        <div>
          <p>{generated_concepts[1].details}</p>
        </div>
      </div>


      <div className={classes.rectangle81}></div>
      <div className={classes.summaryTitle}>
        Summary
      </div>


      {/* <div className={classes.loremIpsumIsSimplyDummyTextOfT}>
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
        industry&#39;s stry. Lorem Ipsum has been the industry&#39;s Lorem Ipsum has been the industry&#39;s{' '}
      </div> */}
      <div className={classes.summaryDetails}>
        <br /><br />
        <div>{generated_summary[0].details}</div>
      </div>
    </div>
  );
});
