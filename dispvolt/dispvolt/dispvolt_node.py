# dispvolt_node.py
# The node that displays the Roomba's battery voltage on the Roomba's LED.
import rclpy  # ROS2のPythonモジュールをインポート
from rclpy.node import Node # rclpy.nodeモジュールからNodeクラスをインポート
from std_msgs.msg import Float32 # トピック通信に使うFloat32メッセージ型をインポート
from std_msgs.msg import UInt8MultiArray # トピック通信に使うUInt8MultiArrayメッセージ型をインポート

class DispVolt(Node): 
    """ルンバのバッテリー電圧のトピックbattery/voltageをサブスクライブしてLEDに表示するクラス    
    """
    def __init__(self):
        """コンストラクタ。サブスクライバーを生成する。
        """
        # Nodeクラスのコンストラクタを呼び出し、'volt_subscriber_node'というノード名をつける。
        super().__init__('disp_volt_node') 
        # サブスクライバーの生成。create_subscriptionの1番目の引数Float32はトピック通信に使うメッセージ型。        
        # 2番目の引数'battery/voltage'はトピック名。
        # 3番目の引数はコールバック関数。 4番目の引数はキューのサイズ。
        self.subscription = self.create_subscription(Float32,'battery/voltage', self.listener_callback, 10)
        # パブリッシャーの生成。create_publisherの1番目の引数はトピック通信に使うメッセージ型。
        # UInt8MultiArray型はLEDに表示するASCIIコードとして通信に使われる。
        # 2番目の引数'set_ascii'はトピック名。
        # 3番目の引数はキューのサイズ。キューサイズはQOS(quality of service)の設定に使われる。
        # サブスクライバーがデータを何らかの理由で受信できないときのキューサイズの上限となる。
        self.publisher = self.create_publisher(UInt8MultiArray,'set_ascii', 10)
        # UInt8MultiArrayメッセージ型オブジェクトの生成。
        self.led = UInt8MultiArray()
        print("*** dispvolt node ***")
   
               
    def listener_callback(self, Float32): 
        """サブスクライバーのコールバック関数。端末にVoltageを表示し、LED表示メッセージをpublishする。
        """
        self.get_logger().info("Voltage: %f" % (Float32.data))
        # LEDに表示するためのASCIIコードのリストを作る。
        self.led.data = []                  # リストを空にする。 
        volt_str = str(Float32.data * 100)  # 小数点は不要なので100倍して4桁にしておく。
        for chardata in volt_str[:4]:       # 先頭から4文字までを取り出しASCIIコードのリストにする。
            self.led.data.append(ord(chardata))
        # LED表示メッセージをパブリッシュ（送信）する。
        self.publisher.publish(self.led)
   
   
def main(args=None):
    rclpy.init(args=args)           # rclpyモジュールの初期化
    volt_subscriber = DispVolt()    # ノードの作成
    rclpy.spin(volt_subscriber)     # コールバック関数が呼び出し
    volt_subscriber.destory_node()  # ノードの破壊
    rclpy.shutdown()                # rclpyモジュールの終了処理

if __name__ == '__main__':
    main()