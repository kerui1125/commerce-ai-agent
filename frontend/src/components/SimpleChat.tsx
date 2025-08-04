import { useState, useEffect, useRef } from 'react';
import {
    Container,
    Header,
    Input,
    Button,
    SpaceBetween,
    Select,
    FileUpload,
    Cards,
    Box,
    Badge
} from '@cloudscape-design/components';
import axios from 'axios';

interface Product {
    id: number;
    title: string;
    price: number;
    description: string;
    image: string;
    category: string;
}

interface ChatMessage {
    type: 'user' | 'bot';
    content: string;
    products?: Product[];
    uploadedImage?: string;
}

export default function SimpleChat() {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [chatType, setChatType] = useState('general_conversation');
    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const chatTypeOptions = [
        { label: 'General Conversation', value: 'general_conversation' },
        { label: 'Product Recommendation', value: 'product_recommendation_text' },
        { label: 'Image Search', value: 'product_search_image' }
    ];

    // Auto-scroll function
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // Auto-scroll when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!message.trim() && files.length === 0) return;

        // Create user message with uploaded image
        const userMessage: ChatMessage = {
            type: 'user',
            content: message || 'Find products like this image',
            uploadedImage: files.length > 0 ? URL.createObjectURL(files[0]) : undefined
        };
        setMessages(prev => [...prev, userMessage]);
        setLoading(true);

        try {
            // Convert file to base64 if needed
            let imageData = null;
            if (files.length > 0 && chatType === 'product_search_image') {
                const file = files[0];
                const reader = new FileReader();
                imageData = await new Promise((resolve) => {
                    reader.onload = () => {
                        const base64 = reader.result as string;
                        resolve(base64.split(',')[1]); // Remove data:image/jpeg;base64, prefix
                    };
                    reader.readAsDataURL(file);
                });
            }

            // Call your backend API - use current server's IP
            const apiUrl = `${window.location.protocol}//${window.location.hostname}:8000/api/chat`;
            const response = await axios.post(apiUrl, {
                message: message,
                type: chatType,
                image: imageData
            });

            // Add bot response
            const botMessage: ChatMessage = {
                type: 'bot',
                content: response.data.response,
                products: response.data.products || []
            };
            setMessages(prev => [...prev, botMessage]);

        } catch (error) {
            console.error('Error:', error);
            const errorMessage: ChatMessage = {
                type: 'bot',
                content: 'Sorry, I encountered an error. Please try again.'
            };
            setMessages(prev => [...prev, errorMessage]);
        }

        setMessage('');
        setFiles([]);
        setLoading(false);
    };

    // Inline styles to prevent auto-formatter issues
    const containerStyle = {
        height: '100vh',
        display: 'flex',
        flexDirection: 'column' as const,
        padding: 0,
        margin: 0
    };

    const contentStyle = {
        height: '100%',
        display: 'flex',
        flexDirection: 'column' as const,
        padding: '16px',
        position: 'relative' as const
    };

    const messagesStyle = {
        flex: 1,
        border: '1px solid #ccc',
        padding: '16px',
        overflowY: 'auto' as const,
        borderRadius: '8px',
        backgroundColor: '#fafafa',
        minHeight: 0,
        maxHeight: 'calc(100vh - 200px)',
        marginBottom: '16px'
    };

    const inputRowStyle = {
        display: 'flex',
        gap: '8px',
        alignItems: 'center'
    };

    const inputStyle = {
        flex: 1
    };

    return (
        <div style={containerStyle}>
            <Container header={<Header>Commerce AI Agent</Header>}>
                <div style={contentStyle}>
                    {/* Chat Type Selector - FIXED AT TOP */}
                    <div style={{
                        marginBottom: '16px',
                        position: 'relative',
                        zIndex: 1000,
                        flexShrink: 0
                    }}>
                        <Select
                            selectedOption={chatTypeOptions.find(opt => opt.value === chatType) || null}
                            onChange={({ detail }) => setChatType(detail.selectedOption.value!)}
                            options={chatTypeOptions}
                            placeholder="Select chat type"
                            expandToViewport={true}
                        />
                    </div>

                    {/* Messages Display - SCROLLABLE AREA ONLY */}
                    <div style={messagesStyle}>
                        {messages.map((msg, index) => (
                            <div key={index} style={{ marginBottom: '16px' }}>
                                <div style={{
                                    backgroundColor: msg.type === 'user' ? '#e3f2fd' : '#f5f5f5',
                                    padding: '12px',
                                    borderRadius: '12px',
                                    maxWidth: '85%',
                                    marginLeft: msg.type === 'user' ? 'auto' : '0',
                                    marginRight: msg.type === 'user' ? '0' : 'auto',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                                }}>
                                    <strong>{msg.type === 'user' ? 'You' : 'AI Agent'}:</strong> {msg.content}

                                    {/* Show uploaded image for user messages */}
                                    {msg.uploadedImage && (
                                        <div style={{ marginTop: '10px' }}>
                                            <img
                                                src={msg.uploadedImage}
                                                alt="Uploaded"
                                                style={{
                                                    maxWidth: '200px',
                                                    maxHeight: '200px',
                                                    objectFit: 'cover' as const,
                                                    borderRadius: '8px',
                                                    border: '1px solid #ddd'
                                                }}
                                            />
                                        </div>
                                    )}
                                </div>

                                {/* Display Products */}
                                {msg.products && msg.products.length > 0 && (
                                    <div style={{ marginTop: '12px' }}>
                                        <Cards
                                            items={msg.products}
                                            cardDefinition={{
                                                header: item => item.title,
                                                sections: [
                                                    {
                                                        content: item => (
                                                            <SpaceBetween size="s">
                                                                <img
                                                                    src={`${window.location.protocol}//${window.location.hostname}:8000/api/proxy-image?url=${encodeURIComponent(item.image)}`}
                                                                    alt={item.title}
                                                                    style={{
                                                                        width: '100%',
                                                                        maxWidth: '150px',
                                                                        height: '150px',
                                                                        objectFit: 'cover' as const,
                                                                        borderRadius: '4px'
                                                                    }}
                                                                />
                                                                <Box fontSize="heading-m" color="text-status-success">
                                                                    ${item.price}
                                                                </Box>
                                                                <Badge color="blue">{item.category}</Badge>
                                                            </SpaceBetween>
                                                        )
                                                    }
                                                ]
                                            }}
                                            cardsPerRow={[
                                                { cards: 1 },
                                                { minWidth: 500, cards: 2 },
                                                { minWidth: 800, cards: 3 }
                                            ]}
                                        />
                                    </div>
                                )}
                            </div>
                        ))}

                        {loading && (
                            <div style={{
                                textAlign: 'center' as const,
                                padding: '20px',
                                color: '#666',
                                fontStyle: 'italic' as const
                            }}>
                                AI is thinking...
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* File Upload for Image Search - FIXED */}
                    {chatType === 'product_search_image' && (
                        <div style={{
                            marginBottom: '16px',
                            flexShrink: 0
                        }}>
                            <FileUpload
                                onChange={({ detail }) => setFiles(detail.value)}
                                value={files}
                                accept="image/*"
                                multiple={false}
                                showFileLastModified
                                showFileSize
                                showFileThumbnail
                                constraintText="Upload an image to search for similar products"
                            />
                        </div>
                    )}

                    {/* Input and Send - FIXED AT BOTTOM */}
                    <div style={{
                        ...inputRowStyle,
                        flexShrink: 0
                    }}>
                        <div style={inputStyle}>
                            <Input
                                value={message}
                                onChange={({ detail }) => setMessage(detail.value)}
                                placeholder="Type your message..."
                                onKeyDown={(e) => e.detail.key === 'Enter' && !loading && handleSend()}
                                disabled={loading}
                            />
                        </div>
                        <Button
                            onClick={handleSend}
                            disabled={loading || (!message.trim() && files.length === 0)}
                            variant="primary"
                        >
                            Send
                        </Button>
                    </div>
                </div>
            </Container>
        </div>
    );
}