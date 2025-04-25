from datasets import load_dataset
import json
import os
import time
from typing import List, Dict, Any
import re

class HeadlineProcessor:
    def __init__(self):
        self.start_time = time.time()
        self.output_dir = 'output'
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_dataset(self) -> Any:
        """加载数据集"""
        print("正在加载数据集...")
        try:
            ds = load_dataset("AdaptLLM/finance-tasks", "Headline")
            return ds['train']
        except Exception as e:
            print(f"加载数据集时出错: {e}")
            return None
    
    def parse_qa_pairs(self, text: str) -> List[Dict[str, str]]:
        """解析文本中的问答对"""
        # 使用正则表达式匹配问答对
        pattern = r'Q(\d+):\s*(.*?)\s*A\1:\s*(.*?)(?=Q\d+:|$)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        qa_pairs = []
        for q_num, question, answer in matches:
            qa_pair = {
                "id": f"{int(q_num):03d}",
                "Question": question.strip(),
                "Answer": answer.strip(),
                "type": "headline",
                "source": "AdaptLLM/finance-tasks"
            }
            qa_pairs.append(qa_pair)
        
        return qa_pairs
    
    def process_dataset(self, dataset: Any) -> List[Dict[str, str]]:
        """处理数据集"""
        print("正在处理数据...")
        all_qa_pairs = []
        
        for item in dataset:
            qa_pairs = self.parse_qa_pairs(item['text'])
            all_qa_pairs.extend(qa_pairs)
        
        return all_qa_pairs
    
    def save_dataset(self, qa_pairs: List[Dict[str, str]], filename: str = 'output/headline_qa.json'):
        """保存数据集到文件"""
        if not qa_pairs:
            return
        
        print("正在保存数据...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filename}")
    
    def generate_report(self, qa_pairs: List[Dict[str, str]]):
        """生成处理报告"""
        end_time = time.time()
        processing_time = end_time - self.start_time
        
        report = {
            "total_qa_pairs": len(qa_pairs),
            "processing_time_seconds": processing_time,
            "processing_time_minutes": processing_time / 60,
            "dataset_info": {
                "name": "AdaptLLM/finance-tasks",
                "subset": "Headline",
                "format_version": "1.0"
            }
        }
        
        # 保存报告
        with open('output/processing_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n处理报告:")
        print(f"总问答对数量: {report['total_qa_pairs']}")
        print(f"处理时间: {report['processing_time_seconds']:.2f} 秒 ({report['processing_time_minutes']:.2f} 分钟)")
    
    def run(self):
        """运行完整的处理流程"""
        # 加载数据集
        dataset = self.load_dataset()
        if not dataset:
            return
        
        # 处理数据
        qa_pairs = self.process_dataset(dataset)
        
        # 保存数据
        self.save_dataset(qa_pairs)
        
        # 生成报告
        self.generate_report(qa_pairs)

def main():
    processor = HeadlineProcessor()
    processor.run()

if __name__ == "__main__":
    main() 