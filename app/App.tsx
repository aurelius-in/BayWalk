import { StatusBar } from 'expo-status-bar';
import { View, Text, Button, Alert } from 'react-native';

async function exportScene() {
  try {
    const scene = { anchors: [{ type: 'bay_rect', width_m: 20, height_m: 10 }], zones: [{ name: 'lane_A' }] };
    const res = await fetch('http://localhost:8080/projects/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scene, name: 'Bay A', targets: { num_cameras: 8, target_fps: 8 } }),
    });
    const json = await res.json();
    Alert.alert('Scene exported', `Project ${json.id} created`);
  } catch (e) {
    Alert.alert('Error', String(e));
  }
}

export default function App() {
  return (
    <View style={{flex:1,justifyContent:'center',alignItems:'center'}}>
      <Text>BayWalk Mobile - MVP</Text>
      <Button title="Export Scene JSON" onPress={exportScene}/>
      <StatusBar style="auto" />
    </View>
  );
}
