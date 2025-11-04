import { useEffect, useState } from 'react';

function SnowEffect({ count = 50 }) {
  const [snowflakes, setSnowflakes] = useState([]);

  useEffect(() => {
    const createSnowflake = (id) => ({
      id,
      left: Math.random() * 100,
      animationDuration: Math.random() * 3 + 5,
      opacity: Math.random() * 0.6 + 0.4,
      fontSize: Math.random() * 10 + 10,
    });

    const initialSnowflakes = Array.from({ length: count }, (_, i) => createSnowflake(i));
    setSnowflakes(initialSnowflakes);

    const interval = setInterval(() => {
      setSnowflakes(prev =>
        prev.map(flake => ({
          ...createSnowflake(flake.id),
          id: flake.id,
        }))
      );
    }, 8000);

    return () => clearInterval(interval);
  }, [count]);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none" style={{ zIndex: 5 }}>
      {snowflakes.map((flake) => (
        <div
          key={flake.id}
          className="snowflake"
          style={{
            left: `${flake.left}%`,
            animationDuration: `${flake.animationDuration}s`,
            opacity: flake.opacity,
            fontSize: `${flake.fontSize}px`,
          }}
        >
          ❄
        </div>
      ))}
    </div>
  );
}

export default SnowEffect;
