# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
import hashlib
import requests
import threading

class RepairApp(App):
    # 安全配置（正式环境建议加密存储）
    SECRET_KEY = StringProperty("wq355tfvfd3542680")
    API_URL = StringProperty("https://www.xiazyba.com/wp-content/plugins/paypy/api/notify/index.php")
    PLUGIN_NAME = StringProperty("paypy")
    
    def build(self):
        """构建移动端优化界面"""
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(1, 1)
        )
        
        # 金额输入区
        input_layout = BoxLayout(
            orientation='vertical',
            spacing=10
        )
        input_layout.add_widget(Label(
            text="金额 (单位：元)",
            font_size='18sp',
            color=get_color_from_hex('#333333'),
            size_hint=(1, None),
            height='30sp'
        ))
        self.amount_input = TextInput(
            text='2.00',
            input_type='number',
            multiline=False,
            font_size='24sp',
            size_hint=(1, None),
            height='60sp',
            hint_text_color=get_color_from_hex('#999999'),
            foreground_color=get_color_from_hex('#333333'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        input_layout.add_widget(self.amount_input)
        main_layout.add_widget(input_layout)
        
        # 支付方式选择
        spinner_layout = BoxLayout(
            orientation='vertical',
            spacing=10
        )
        spinner_layout.add_widget(Label(
            text="支付方式",
            font_size='18sp',
            color=get_color_from_hex('#333333'),
            size_hint=(1, None),
            height='30sp'
        ))
        self.type_spinner = Spinner(
            values=('wechat', 'alipay'),
            text='wechat',
            font_size='18sp',
            size_hint=(1, None),
            height='50sp',
            background_color=get_color_from_hex('#F5F5F5'),
            option_cls=SpinnerOption(
                background_color=get_color_from_hex('#FFFFFF'),
                font_size='16sp'
            )
        )
        spinner_layout.add_widget(self.type_spinner)
        main_layout.add_widget(spinner_layout)
        
        # 操作按钮
        self.action_btn = Button(
            text="执行补单操作",
            font_size='20sp',
            size_hint=(1, None),
            height='70sp',
            background_color=get_color_from_hex('#4CAF50'),
            background_normal='',
            color=get_color_from_hex('#FFFFFF')
        )
        self.action_btn.bind(on_press=self.start_async_repair)
        main_layout.add_widget(self.action_btn)
        
        # 状态显示
        self.status_label = Label(
            text="就绪状态",
            font_size='16sp',
            color=get_color_from_hex('#666666'),
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height='40sp'
        )
        main_layout.add_widget(self.status_label)
        
        return main_layout

    def start_async_repair(self, instance):
        """启动异步补单流程"""
        self.action_btn.disabled = True
        self.update_status("正在验证输入...", '#2196F3')
        threading.Thread(target=self.execute_repair).start()

    def execute_repair(self):
        """补单核心业务逻辑"""
        try:
            # 获取输入参数
            amount = self.amount_input.text.strip()
            pay_type = self.type_spinner.text
            
            # 输入验证
            if not self.validate_amount(amount):
                return
                
            # 生成安全签名
            signature = self.generate_signature(amount, pay_type)
            
            # 网络请求
            self.update_status("正在连接服务器...", '#2196F3')
            response = requests.get(
                self.API_URL,
                params={
                    'price': amount,
                    'type': pay_type,
                    'plugin': self.PLUGIN_NAME,
                    'sign': signature
                },
                timeout=15
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 1:
                    self.show_success("补单成功！")
                else:
                    self.show_error(f"服务器返回错误：{result.get('msg', '未知错误')}")
            else:
                self.show_error(f"网络错误：HTTP {response.status_code}")
                
        except Exception as e:
            self.show_error(f"系统异常：{str(e)}")
        finally:
            self.reset_ui()

    def validate_amount(self, amount):
        """金额格式验证"""
        if not amount.replace('.', '', 1).isdigit():
            self.show_error("金额格式错误，示例：2.00")
            return False
        if float(amount) <= 0:
            self.show_error("金额必须大于零")
            return False
        return True

    def generate_signature(self, price, pay_type):
        """双重MD5签名生成"""
        stage1 = hashlib.md5(f"{price}{pay_type}".encode()).hexdigest()
        return hashlib.md5(
            f"{stage1}{self.SECRET_KEY}{self.PLUGIN_NAME}".encode()
        ).hexdigest()

    def update_status(self, message, color_code='#666666'):
        """线程安全的状态更新"""
        def update_ui(dt):
            self.status_label.text = message
            self.status_label.color = get_color_from_hex(color_code)
        Clock.schedule_once(update_ui)

    def show_success(self, message):
        """成功状态处理"""
        self.update_status(message, '#4CAF50')
        Clock.schedule_once(lambda dt: self.reset_ui(), 3)

    def show_error(self, error_msg):
        """错误处理"""
        self.update_status(error_msg, '#F44336')
        Clock.schedule_once(lambda dt: self.reset_ui(), 5)

    def reset_ui(self):
        """重置界面状态"""
        def reset(dt):
            self.action_btn.disabled = False
            self.status_label.text = "就绪状态"
            self.status_label.color = get_color_from_hex('#666666')
        Clock.schedule_once(reset)

if __name__ == '__main__':
    RepairApp().run()
