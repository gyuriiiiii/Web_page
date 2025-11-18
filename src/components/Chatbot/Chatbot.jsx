// src/components/Chatbot/Chatbot.jsx
import { useState, useRef, useEffect } from "react";
import styles from "./Chatbot.module.css";

// chatbot 호출 
async function backendGetReply(userText) {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText }),
    });

    const data = await res.json();

    if (data.reply) return data.reply;
    return "⚠️ 서버 응답이 비정상입니다.";
  } catch (err) {
    return "⚠️ 서버와 연결할 수 없습니다.";
  }
}


export default function Chatbot({
  title = "Yeobaek Chat-bot",
  subtitle = "실험용 UI v1",
  getReply = backendGetReply, 
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "bot",
      text:
        "안녕하세요! 😊\n" +
        "지금은 데모 버전이라, 간단한 질문에만 하드코딩으로 답해요.\n" +
        "조금만 기다려주세요!.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);

  // 새 메시지 올 때마다 맨 아래로 스크롤
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleToggle = () => {
    setIsOpen((prev) => !prev);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || isSending) return;

    const userMsg = {
      id: Date.now(),
      role: "user",
      text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsSending(true);

    // 데모: 살짝 딜레이 후 응답
    setTimeout(async () => {
      const replyText = await getReply(text);
      const botMsg = {
        id: Date.now() + 1,
        role: "bot",
        text: replyText,
      };
      setMessages((prev) => [...prev, botMsg]);
      setIsSending(false);
    }, 400);
  };

  return (
    <>
      {/* 오른쪽 아래 토글 버튼 */}
      <button
        type="button"
        className={styles.toggleButton}
        onClick={handleToggle}
      >
        💬 Chat-bot
      </button>

      {/* 챗봇 창 */}
      {isOpen && (
        <div className={styles.window}>
          <div className={styles.header}>
            <div>
              <span className={styles.titleMain}>{title}</span>
              <span className={styles.titleSub}>{subtitle}</span>
            </div>
            <button
              type="button"
              className={styles.closeButton}
              onClick={handleToggle}
            >
              ×
            </button>
          </div>

          <div className={styles.messages}>
            {messages.map((m) => (
              <div
                key={m.id}
                className={`${styles.message} ${
                  m.role === "user" ? styles.user : styles.bot
                }`}
              >
                <div className={styles.bubble}>
                  {m.text.split("\n").map((line, i) => (
                    <span key={i}>
                      {line}
                      <br />
                    </span>
                  ))}
                </div>
                <div className={styles.meta}>
                  {m.role === "user" ? "You" : "Bot · demo"}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form className={styles.inputArea} onSubmit={handleSubmit}>
            <input
              className={styles.input}
              type="text"
              placeholder={
                isSending ? "응답 생성 중..." : "메시지를 입력하세요..."
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isSending}
              autoComplete="off"
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isSending}
            >
              {isSending ? "..." : "전송"}
            </button>
          </form>
        </div>
      )}
    </>
  );
}