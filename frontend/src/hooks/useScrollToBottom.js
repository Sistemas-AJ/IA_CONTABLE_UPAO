import { useRef, useEffect } from 'react';

const useScrollToBottom = (dependencies) => {
  const endRef = useRef(null);

  useEffect(() => {
    if (endRef.current) {
      endRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [dependencies]);

  return endRef;
};

export default useScrollToBottom;