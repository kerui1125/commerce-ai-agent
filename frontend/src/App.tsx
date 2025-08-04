import '@cloudscape-design/global-styles/index.css';
import { AppLayout, TopNavigation } from '@cloudscape-design/components';
import SimpleChat from './components/SimpleChat';

function App() {
  return (
    <div style={{ height: '100vh', margin: 0, padding: 0 }}>
      <TopNavigation
        identity={{
          href: "/",
          title: "Commerce AI Agent"
        }}
      />
      <AppLayout
        navigationHide={true}
        toolsHide={true}
        content={<SimpleChat />}
        disableContentPaddings={true}
      />
    </div>
  );
}

export default App;
