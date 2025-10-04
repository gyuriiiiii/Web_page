import SplitText from './SplitText';
import Squares from './Squares';

function App() {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: '#0a0a0f',
      overflow: 'hidden',
      margin: 0,
      padding: 0
    }}>
      <Squares
        speed={0.3}
        squareSize={60}
        direction='diagonal'
        borderColor='#09402C'
        hoverFillColor='#404b3eff'
      />

      <nav style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 20,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '1rem clamp(1rem, 5vw, 4rem)',
        background: 'rgba(66, 92, 76, 0.3)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.1)'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.3rem',
          color: '#fff',
          fontSize: 'clamp(1.3rem, 2.5vw, 1.5rem)',
          fontWeight: 600
        }}>
          <img src="/logo.png" alt="Yeobaek Logo" style={{ height: '30px' }} />
          Yeobaek
        </div>
        <div style={{
          display: 'flex',
          gap: 'clamp(1rem, 3vw, 2rem)',
          color: '#fff',
          fontSize: 'clamp(0.9rem, 1.5vw, 1rem)'
        }}>
          <a href="#" style={{ color: '#fff', textDecoration: 'none', opacity: 0.9, fontSize: '1rem' }}>Home</a>
          <a href="#" style={{ color: '#fff', textDecoration: 'none', opacity: 0.9, fontSize: '1rem' }}>LAB</a>
          <a href="#" style={{ color: '#fff', textDecoration: 'none', opacity: 0.9, fontSize: '1rem' }}>Service</a>
          <a href="#" style={{ color: '#fff', textDecoration: 'none', opacity: 0.9, fontSize: '1rem' }}>About</a>
        </div>
      </nav>

      <div style={{
        position: 'relative',
        zIndex: 10,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        color: '#fff',
        textAlign: 'center',
        padding: '1rem'
      }}>
        <h1 style={{
          fontSize: 'clamp(2rem, 8vw, 4.5rem)',
          marginBottom: '1rem',
          fontWeight: 700,
          lineHeight: 1.5,
          maxWidth: '900px',
          padding: '0 1rem'
        }}>
          <SplitText text="Yeobaek Web" delay={50} />
        </h1>

        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '1rem',
          marginTop: '2rem',
          justifyContent: 'center'
        }}>
          <button style={{
            background: '#fff',
            color: '#000',
            border: 'none',
            padding: 'clamp(0.8rem, 2vw, 1rem) clamp(1.5rem, 4vw, 2.5rem)',
            borderRadius: '50px',
            fontSize: 'clamp(0.9rem, 1.5vw, 1rem)',
            fontWeight: 600,
            cursor: 'pointer'
          }}>
            LAB 구경하기
          </button>
          <button style={{
            background: 'transparent',
            color: '#fff',
            border: '1px solid rgba(255,255,255,0.2)',
            padding: 'clamp(0.8rem, 2vw, 1rem) clamp(1.5rem, 4vw, 2.5rem)',
            borderRadius: '50px',
            fontSize: 'clamp(0.9rem, 1.5vw, 1rem)',
            fontWeight: 600,
            cursor: 'pointer',
            backdropFilter: 'blur(10px)'
          }}>
            Service 구경하기
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;