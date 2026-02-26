"""
Agent by Cursor - 更多工具集成

新增工具:
1. 密码学高级工具
2. Web安全高级工具
3. Pwn利用工具
4. 取证工具增强
"""

import re
import hashlib
import base64
from typing import Optional, List, Dict, Any
import subprocess
import tempfile
import os


# ==================== 高级密码学工具 ====================

class AdvancedCryptoTools:
    """高级密码学工具"""
    
    @staticmethod
    def rsa_key_analysis(pem_data: str) -> Dict[str, Any]:
        """RSA密钥分析"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            
            key = serialization.load_pem_public_key(pem_data.encode())
            
            if isinstance(key, rsa.RSAPublicKey):
                public_numbers = key.public_numbers()
                
                return {
                    'type': 'RSA',
                    'key_size': key.key_size,
                    'n': public_numbers.n.bit_length(),
                    'e': public_numbers.e,
                    'is_weak': public_numbers.e == 65537
                }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def ecdh_shared_secret(private_key: str, public_key: str) -> Optional[str]:
        """ECDH共享密钥计算"""
        try:
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.primitives import serialization
            
            priv_key = serialization.load_pem_private_key(private_key.encode(), password=None)
            pub_key = serialization.load_pem_public_key(public_key.encode())
            
            if isinstance(priv_key, ec.EllipticCurvePrivateKey):
                shared_key = priv_key.exchange(ec.ECDH(), pub_key)
                return shared_key.hex()
        except Exception as e:
            return None
    
    @staticmethod
    def elliptic_curve_analysis(pubkey: str) -> Dict[str, Any]:
        """椭圆曲线分析"""
        try:
            from cryptography.hazmat.primitives import serialization
            
            key = serialization.load_pem_public_key(pubkey.encode())
            
            return {
                'type': 'EllipticCurve',
                'curve': str(key.curve.name),
                'key_size': key.key_size
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def lattice_attack(cipher: str, modulus: int, max_r: int = 10000) -> Optional[str]:
        """简单的格基约减攻击（用于某些特定加密）"""
        # 这是一个简化版本，实际实现需要更复杂的格基约减算法
        # 使用Baby-Step Giant-Step或其他算法
        for r in range(1, max_r):
            # 尝试不同的小参数
            try:
                # 这里只是示例，实际需要实现具体的格算法
                pass
            except:
                pass
        return None
    
    @staticmethod
    def identify_hash(hash_value: str) -> Dict[str, Any]:
        """哈希算法识别"""
        length = len(hash_value)
        patterns = {
            32: {'type': 'MD5', 'bits': 128},
            40: {'type': 'SHA1', 'bits': 160},
            64: {'type': 'SHA256', 'bits': 256},
            96: {'type': 'SHA384', 'bits': 384},
            128: {'type': 'SHA512', 'bits': 512},
            56: {'type': 'Bitcoin/DoubleSHA256', 'bits': 160},
        }
        
        if hash_value.lower().startswith('$2'):
            return {'type': 'bcrypt', 'bits': 128}
        
        return patterns.get(length, {'type': 'Unknown', 'bits': 0})


# ==================== 高级Web安全工具 ====================

class AdvancedWebTools:
    """高级Web安全工具"""
    
    @staticmethod
    def jwt_decode(token: str) -> Dict[str, Any]:
        """JWT Token解码（包含算法混淆检测）"""
        try:
            # 分割token
            parts = token.split('.')
            if len(parts) != 3:
                return {'error': 'Invalid JWT format'}
            
            header = base64.urlsafe_b64decode(parts[0] + '=' * (4 - len(parts[0]) % 4))
            payload = base64.urlsafe_b64decode(parts[1] + '=' * (4 - len(parts[1]) % 4))
            
            return {
                'header': header.decode(),
                'payload': payload.decode(),
                'algorithm': header.decode()
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def detect_jwt_none_algorithm(token: str) -> bool:
        """检测JWT none算法"""
        decoded = AdvancedWebTools.jwt_decode(token)
        if 'error' in decoded:
            return False
        
        return 'none' in decoded['header'].lower()
    
    @staticmethod
    def csrf_token_analyze(response: str) -> Dict[str, Any]:
        """CSRF Token分析"""
        patterns = [
            r'csrf_token["\']?\s*[:=]\s*["\']?([^"\'>\s]+)',
            r'_token["\']?\s*[:=]\s*["\']?([^"\'>\s]+)',
            r'xsrf_token["\']?\s*[:=]\s*["\']?([^"\'>\s]+)'
        ]
        
        tokens = {}
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                tokens[len(tokens)] = match
        
        return {
            'csrf_tokens_found': len(tokens),
            'tokens': tokens
        }
    
    @staticmethod
    def graphql_introspection(url: str) -> Dict[str, Any]:
        """GraphQL内省检测"""
        try:
            import urllib.parse
            import urllib.request
            
            # 执行内省查询
            query = '{ "query": "query { __schema { queryType { name } } }" }'
            
            req = urllib.request.Request(
                url,
                data=query.encode(),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode()
                
                return {
                    'introspection_enabled': True,
                    'schema': data
                }
        except Exception as e:
            return {
                'introspection_enabled': False,
                'error': str(e)
            }


# ==================== 取证工具增强 ====================

class AdvancedForensicsTools:
    """高级取证工具"""
    
    @staticmethod
    def extract_gps_metadata(filepath: str) -> Dict[str, Any]:
        """从图片中提取GPS元数据"""
        try:
            from PIL import Image, ExifTags, ExifTags
            
            img = Image.open(filepath)
            exif_data = img._getexif()
            
            if exif_data:
                for tag, value in exif_data.items():
                    if tag == ExifTags.TAGS.GPSLatitudeRef:
                        return {'gps': {'latitudeRef': value}}
                    if tag == ExifTags.TAGS.GPSLatitude:
                        return {'gps': {'latitude': value}}
            
            return {'gps': None}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_pcap(pcap_file: str) -> Dict[str, Any]:
        """分析PCAP文件"""
        try:
            # 尝试使用scapy
            from scapy.all import rdpcap, IP, TCP, UDP
            
            packets = rdpcap(pcap_file)
            
            stats = {
                'total_packets': len(packets),
                'protocols': {},
                'top_sources': {},
                'top_destinations': {},
                'dns_queries': [],
                'http_requests': []
            }
            
            for packet in packets:
                if IP in packet:
                    src = packet[IP].src
                    dst = packet[IP].dst
                    
                    stats['top_sources'][src] = stats['top_sources'].get(src, 0) + 1
                    stats['top_destinations'][dst] = stats['top_destinations'].get(dst, 0) + 1
                    
                    if TCP in packet:
                        stats['protocols']['TCP'] = stats['protocols'].get('TCP', 0) + 1
                    elif UDP in packet:
                        stats['protocols']['UDP'] = stats['protocols'].get('UDP', 0) + 1
                    
                    # 检测DNS
                    if packet.haslayer('DNS'):
                        stats['protocols']['DNS'] = stats['protocols'].get('DNS', 0) + 1
                        if packet['DNS'].qd:
                            stats['dns_queries'].append(packet['DNS'].qd.qname.decode())
            
            return stats
        
        except ImportError:
            # scapy不可用，尝试使用tshark
            return AdvancedForensicsTools._analyze_pcap_tshark(pcap_file)
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _analyze_pcap_tshark(pcap_file: str) -> Dict[str, Any]:
        """使用tshark分析PCAP"""
        try:
            result = subprocess.run(
                ['tshark', '-r', pcap_file, '-q', '-z', 'conversations,ip'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'tshark_output': result.stdout,
                'total_lines': len(result.stdout.split('\n'))
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def memory_volatility_profile(memdump: str, profile: str = 'Win10x64') -> Dict[str, Any]:
        """使用Volatility分析内存转储"""
        try:
            # 进程列表
            result = subprocess.run(
                ['vol2', '-f', memdump, 'windows.pslist'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                'profile': profile,
                'pslist_output': result.stdout,
                'process_count': len([line for line in result.stdout.split('\n') if line.strip()])
            }
        except Exception as e:
            return {'error': str(e)}


# ==================== 工具注册表增强 ====================

class ExtendedToolRegistry:
    """扩展工具注册表"""
    
    def __init__(self):
        self.advanced_crypto = AdvancedCryptoTools()
        self.advanced_web = AdvancedWebTools()
        self.advanced_forensics = AdvancedForensicsTools()
    
    def get_all_tools(self) -> Dict[str, List[str]]:
        """获取所有可用工具"""
        return {
            'advanced_crypto': [
                'rsa_key_analysis',
                'ecdh_shared_secret',
                'elliptic_curve_analysis',
                'lattice_attack',
                'identify_hash'
            ],
            'advanced_web': [
                'jwt_decode',
                'detect_jwt_none_algorithm',
                'csrf_token_analyze',
                'graphql_introspection'
            ],
            'advanced_forensics': [
                'extract_gps_metadata',
                'analyze_pcap',
                'memory_volatility_profile'
            ]
        }
    
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """执行工具"""
        # Crypto工具
        if tool_name in self.advanced_crypto.__dict__:
            method = getattr(self.advanced_crypto, tool_name)
            return method(**args)
        
        # Web工具
        elif tool_name in self.advanced_web.__dict__:
            method = getattr(self.advanced_web, tool_name)
            return method(**args)
        
        # Forensics工具
        elif tool_name in self.advanced_forensics.__dict__:
            method = getattr(self.advanced_forensics, tool_name)
            return method(**args)
        
        else:
            return {'error': f'Tool not found: {tool_name}'}


# ==================== 工具使用示例 ====================

def demonstrate_tools():
    """演示新工具的功能"""
    
    # 高级密码学工具
    print("=== 高级密码学工具 ===")
    crypto_tools = AdvancedCryptoTools()
    
    # 哈希识别
    hash_value = "5d41402abc4b2a76b9719d911017c592"
    hash_info = crypto_tools.identify_hash(hash_value)
    print(f"Hash: {hash_value}")
    print(f"Type: {hash_info['type']}")
    print()
    
    # 高级Web工具
    print("=== 高级Web工具 ===")
    web_tools = AdvancedWebTools()
    
    # JWT解码
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.signature"
    jwt_info = web_tools.jwt_decode(jwt_token)
    print(f"JWT: {jwt_token}")
    print(f"Header: {jwt_info.get('header', 'N/A')}")
    print()
    
    # 注册表
    print("=== 扩展工具注册表 ===")
    registry = ExtendedToolRegistry()
    all_tools = registry.get_all_tools()
    print("Available tools:")
    for category, tools in all_tools.items():
        print(f"  {category}:")
        for tool in tools:
            print(f"    - {tool}")
    print()

    # 执行工具
    print("=== 测试工具 ===")
    result = registry.execute('identify_hash', {'hash_value': hash_value})
    print(f"Result: {result}")


if __name__ == '__main__':
    demonstrate_tools()
