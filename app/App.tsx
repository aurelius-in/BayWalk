import { StatusBar } from 'expo-status-bar';
import { View, Text, Button } from 'react-native';
export default function App() {
  return (
    <View style={{flex:1,justifyContent:'center',alignItems:'center'}}>
      <Text>BayWalk Mobile - MVP</Text>
      <Button title="Export Scene JSON" onPress={()=>{}}/>
      <StatusBar style="auto" />
    </View>
  );
}
