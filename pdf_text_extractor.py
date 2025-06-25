import subprocess
import sys
import os
import time
from datetime import datetime

def install_required_packages():
    """
    必要なパッケージをインストールする関数
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 必要なライブラリをインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] PyPDF2のインストールが完了しました")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] エラー: パッケージのインストールに失敗しました: {e}")
        return False
    return True

def extract_text_from_pdf_with_progress(pdf_path):
    """
    PDFファイルからテキストを抽出し、進捗をリアルタイムで表示する関数
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PDFファイルの読み込みを開始: {pdf_path}")
    
    # PyPDF2をインポート（インストール後）
    try:
        import PyPDF2
    except ImportError:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] エラー: PyPDF2のインポートに失敗しました")
        return None
    
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 総ページ数: {total_pages}")
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                
                # 進捗表示
                progress = (i + 1) / total_pages * 100
                bar_length = 50
                filled_length = int(bar_length * (i + 1) // total_pages)
                bar = '#' * filled_length + '-' * (bar_length - filled_length)
                
                sys.stdout.write(f"\r[{datetime.now().strftime('%H:%M:%S')}] 進捗: [{bar}] {progress:.1f}% (ページ {i+1}/{total_pages})")
                sys.stdout.flush()
                
                time.sleep(0.05)  # 進捗表示を見やすくするための短い待機
            
            print()  # 改行
            print(f"[{datetime.now().strftime('%H:%M:%S')}] テキスト抽出完了")
            
    except Exception as e:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] エラー: テキスト抽出中にエラーが発生しました: {e}")
        return None
    
    return text

def save_text_to_file(text, pdf_path):
    """
    抽出したテキストを同じフォルダにテキストファイルとして保存する関数
    """
    try:
        # PDFファイルと同じフォルダにテキストファイルを保存
        folder_path = os.path.dirname(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_filename = f"{base_name}_extracted.txt"
        txt_path = os.path.join(folder_path, txt_filename)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] テキストファイルを保存中: {txt_path}")
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"PDFファイル: {os.path.basename(pdf_path)}\n")
            f.write(f"抽出日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(text)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 保存完了")
        return txt_path
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] エラー: ファイル保存中にエラーが発生しました: {e}")
        return None

def process_single_pdf():
    """
    単一のPDF処理を実行する関数
    """
    # PDFファイルのパス入力
    pdf_path = input('PDFファイルのパスを入力してください（""で囲んでも囲まなくても可）: ').strip().strip('"\'')
    
    # ファイルの存在確認
    if not os.path.exists(pdf_path):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] エラー: 指定されたファイルが見つかりません: {pdf_path}")
        print("ファイルパスを確認してください。")
        return False
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] エラー: PDFファイルを指定してください。")
        return False
    
    # テキスト抽出の実行
    extracted_text = extract_text_from_pdf_with_progress(pdf_path)
    
    if extracted_text is None:
        print("❌ テキスト抽出に失敗しました。")
        return False
    
    # テキストファイルとして保存
    saved_path = save_text_to_file(extracted_text, pdf_path)
    
    if saved_path:
        print(f"\n✅ 処理完了!")
        print(f"📄 元ファイル: {pdf_path}")
        print(f"💾 保存先: {saved_path}")
        print(f"📊 抽出文字数: {len(extracted_text)} 文字")
        return True
    else:
        print("❌ ファイル保存中にエラーが発生しました。")
        return False

def main_process():
    """
    メイン処理関数（ループ処理）
    """
    print("=" * 60)
    print("PDFテキスト抽出ツール")
    print("=" * 60)
    
    # 必要なパッケージのインストール（初回のみ）
    if not install_required_packages():
        print("❌ パッケージのインストールに失敗しました。処理を終了します。")
        return
    
    # 処理ループ
    while True:
        print("\n" + "-" * 60)
        
        try:
            # PDF処理の実行
            success = process_single_pdf()
            
            if success:
                print("\n" + "=" * 60)
                print("✅ 処理が正常に完了しました！")
            else:
                print("\n" + "=" * 60)
                print("⚠️  処理中にエラーが発生しました。")
            
        except Exception as e:
            print(f"\n予期しないエラーが発生しました: {e}")
        
        # 続行確認
        print("\n" + "=" * 60)
        print("次の操作を選択してください:")
        print("1. 別のPDFファイルを処理する")
        print("2. プログラムを終了する")
        
        while True:
            choice = input("選択してください (1 または 2): ").strip()
            
            if choice == '1':
                print("\n🔄 新しいPDFファイルの処理を開始します...")
                break
            elif choice == '2':
                print("\n👋 プログラムを終了します。ご利用ありがとうございました！")
                return
            else:
                print("❌ 無効な選択です。1 または 2 を入力してください。")

def main():
    """
    プログラムのエントリーポイント
    """
    # プログラム実行確認
    response = input("このプログラムを実行しますか？ (Y/N): ").strip().upper()
    
    if response != 'Y':
        print("プログラムを終了します。")
        return
    
    # メイン処理の実行
    main_process()

# プログラム実行
if __name__ == "__main__":
    main()
