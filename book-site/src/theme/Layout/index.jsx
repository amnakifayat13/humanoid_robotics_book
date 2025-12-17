import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function Layout(props) {
  return (
    <OriginalLayout {...props}>
      {props.children}
      
      <BrowserOnly fallback={null}>
        {() => {
          // Dynamic require: Yeh initialization error ko bypass karta hai
          const BookChatbot = require('@site/src/components/BookChatbot').default;
          return <BookChatbot />;
        }}
      </BrowserOnly>
    </OriginalLayout>
  );
}