using System;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;

namespace TTN_MQTT_Lab
{
    class Program
    {
        private static readonly string MQTT_HOST = "eu1.cloud.thethings.network";
        private static readonly int MQTT_PORT = 8883;
        private static readonly string USERNAME = "safiyo-applcation@ttn";
        private static readonly string PASSWORD = "NNSXS.43GP4YCGCFIXFQKKKE3K7QORHHZLUUWS6I6GUIY.OK4PHULALVJX7G6SHIQBIFWGWPROHG75Q2KM4QLWATMN5DEVSDYA";

        static async Task Main(string[] args)
        {
            Console.WriteLine("MQTTnet ConsoleApp - A The Things Network V3 C# App");
            Console.WriteLine("Press return to exit!");

            // Skapa MQTT-klient
            var mqttFactory = new MqttFactory();
            var mqttClient = mqttFactory.CreateMqttClient();

            // MQTT-anslutningsinställningar
            var mqttOptions = new MqttClientOptionsBuilder()
                .WithClientId(Guid.NewGuid().ToString())
                .WithTcpServer(MQTT_HOST, MQTT_PORT)
                .WithCredentials(USERNAME, PASSWORD)
                .WithTls()
                .Build();

            mqttClient.ConnectedAsync += async e =>
            {
                Console.WriteLine("MQTTnet Client -> Connected with result: Success");
                string topicFilter = "v3/+/devices/+/up"; // TTN topic
                await mqttClient.SubscribeAsync(topicFilter);
                Console.WriteLine($"Subscribed to topic: {topicFilter}");
            };

            mqttClient.ApplicationMessageReceivedAsync += async e =>
            {
                string topic = e.ApplicationMessage.Topic;
                var payload = e.ApplicationMessage.Payload;

                Console.WriteLine($"\nReceived Message:");
                Console.WriteLine($"Topic: {topic}");

                try
                {
                    // Parse JSON payload
                    var jsonDoc = JsonDocument.Parse(Encoding.UTF8.GetString(payload));
                    string frmPayload = jsonDoc.RootElement
                        .GetProperty("uplink_message")
                        .GetProperty("frm_payload")
                        .GetString();

                    // Decode Base64 payload
                    byte[] decodedPayload = Convert.FromBase64String(frmPayload);

                    Console.WriteLine($"Payload (Raw Bytes): {BitConverter.ToString(decodedPayload)}");

                    // Decode and print payload values
                    DecodeAndPrintPayload(decodedPayload);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error parsing or decoding payload: {ex.Message}");
                }

                await Task.CompletedTask;
            };

            try
            {
                await mqttClient.ConnectAsync(mqttOptions);
                Console.WriteLine("Connected to TTN V3 MQTT Broker: " + MQTT_HOST);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Connection failed: {ex.Message}");
                return;
            }

            Console.WriteLine("Waiting for messages...");
            Console.ReadLine();
        }

        public static void DecodeAndPrintPayload(byte[] payload)
        {
            if (payload.Length != 12)
            {
                Console.WriteLine($"Unexpected payload length: {payload.Length} bytes. Ignoring message.");
                return;
            }

            try
            {
                // Decode individual parts of the payload
                float temperature = DecodeIEEE754(payload, 0); // Bytes 0-3
                float humidity = DecodeIEEE754(payload, 4);    // Bytes 4-7
                float ledBrightness = DecodeIEEE754(payload, 8); // Bytes 8-11

                // Print the decoded data
                Console.WriteLine("-- Decoded Payload --");
                Console.WriteLine($"Temperature: {temperature:F2} °C");
                Console.WriteLine($"Humidity: {humidity:F2} %");
                Console.WriteLine($"LED Brightness: {ledBrightness:F2}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error decoding payload: {ex.Message}");
            }
        }

        public static float DecodeIEEE754(byte[] payload, int startIndex)
        {
            if (payload.Length < startIndex + 4)
                throw new ArgumentException("Payload too small for IEEE-754 decoding.");

            byte[] data = new byte[4];
            Array.Copy(payload, startIndex, data, 0, 4);

            // Adjust endianness if system uses Little Endian
            if (BitConverter.IsLittleEndian)
                Array.Reverse(data);

            return BitConverter.ToSingle(data, 0);

        }
    }
}
