import SplitText from './SplitText';
import SnowEffect from './SnowEffect';
import ServiceSections from './components/ServiceSections';  // ← 이 부분 수정

function App() {
  return (
    <div className="w-screen min-h-screen bg-gray-50 m-0 p-0 overflow-x-hidden">
      {/* Hero Section with Image Background */}
      <div className="relative w-screen h-screen overflow-hidden">
        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url(/gomdol.jpg)',
            filter: 'brightness(0.9)',
          }}
        />

        {/* Dark Overlay */}
        <div className="absolute inset-0" /> 

        {/* Snow Effect */}
        <SnowEffect count={50} />
        
        {/* Navigation */}
        <nav className="absolute top-0 left-0 right-0 z-20 flex justify-between items-center px-4 py-4 md:px-16 bg-emerald-900/30 backdrop-blur-xl border-b border-white/10">
          <div className="flex items-center gap-5 text-white text-xl md:text-2xl font-semibold">
            <img src="/logo.png" alt="Yeobaek Logo" className="h-8" />
            Yeobaek
          </div>
          <div className="flex gap-4 md:gap-8 text-white text-sm md:text-base">
            <a href="#home" className="text-white no-underline opacity-90 hover:opacity-100 transition-opacity">Home</a>
            <a href="#service" className="text-white no-underline opacity-90 hover:opacity-100 transition-opacity">Service</a>
            <a href="#about" className="text-white no-underline opacity-90 hover:opacity-100 transition-opacity">About</a>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="relative z-10 flex flex-col gap-7 items-center justify-center h-screen text-gray-600 text-center px-4 pt-20 md:items-end md:pr-32">
          <h1 className="text-7xl md:text-8xl mb-4 font-bold leading-tight max-w-4xl">
            <SplitText text="Yeobaek Web" delay={50} />
          </h1>

          <div className="flex flex-wrap gap-4 mt-8 justify-center md:justify-end">
            <button
              onClick={() => document.getElementById('service')?.scrollIntoView({ behavior: 'smooth' })}
              className="bg-gray-300 text-black border-none px-6 py-3 md:px-10 md:py-4 rounded-full text-sm md:text-base font-semibold cursor-pointer transition-transform hover:scale-105"
            >
              Service 구경하기
            </button>
            <button
              onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
              className="bg-transparent text-gray-800 border border-gray-700 px-6 py-3 md:px-10 md:py-4 rounded-full text-sm md:text-base font-semibold cursor-pointer backdrop-blur-xl transition-all hover:scale-105 hover:border-gray-600"
            >
              About 구경하기
            </button>
          </div>

          {/* Scroll Indicator */}
          <div 
            className="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce cursor-pointer"
            onClick={() => document.getElementById('service')?.scrollIntoView({ behavior: 'smooth' })}
          >
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>
            </svg>
          </div>
        </div>
      </div>

      {/* Service Sections */}
      <div id="service">
        <ServiceSections />
      </div>
    </div>
  );
}

export default App;