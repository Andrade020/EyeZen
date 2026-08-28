# EyeZen
Filtros confortáveis para longos tempos de leitura no Computador!

# 🟢 Filtro de Visão Confortável - Versão Profissional

**Lucas Andrade Desenvolvimento de Softwares**

Aplicativo profissional para Windows que aplica filtros de tela para reduzir fadiga visual.

> 🦀 Existe uma reescrita em Rust (v2, mais rápida e leve) em **[EyeZen2](https://github.com/Andrade020/EyeZen2)**.

---

## 📥 Download

A forma mais rápida de usar o EyeZen é baixar o executável pronto — não precisa instalar Python nem nada:

### **[⬇️ Baixar a última versão na página de Releases](https://github.com/Andrade020/EyeZen/releases)**

Baixe o `.exe` mais recente, execute e pronto.

---

## ▶️ Primeira Execução

Ao abrir o EyeZen, ele **fica rodando discretamente na bandeja do sistema** (perto do relógio, no canto inferior direito do Windows) — não é uma janela grande que fica aberta na tela. Procure o ícone do EyeZen na bandeja.

Clique com o botão direito no ícone da bandeja para:
- ✅ Mudar de filtro rapidamente
- 🖥️ Abrir o painel completo
- ℹ️ Ver informações e atalhos
- ❌ Fechar o aplicativo

### 🎮 Atalhos Globais de Teclado
Funcionam em qualquer lugar do Windows, mesmo com o EyeZen minimizado na bandeja:

| Atalho | Filtro |
|---|---|
| `Ctrl + Alt + 1` | 🌙 Noturno Suave |
| `Ctrl + Alt + 2` | 🟢 Leitura Verde |
| `Ctrl + Alt + 3` | 🟡 Papel Creme |
| `Ctrl + Alt + 4` | 🔘 Desativado |

Mais filtros (☀️ Fique Acordado, 🌈 Modo Feliz, 💜 Modo Crepúsculo, 🎨 Sépia Clássico) ficam disponíveis pelo menu da bandeja.

---

## ✨ Recursos

- ✅ **Execução na Bandeja do Sistema** - Fica rodando discretamente
- ✅ **Atalhos Globais de Teclado** - Mude filtros sem abrir a janela
- ✅ **Ícone Personalizado** - Logo da sua empresa no executável
- ✅ **Salvamento Automático** - Lembra o último filtro usado
- ✅ **Interface Moderna** - Design intuitivo
- ✅ **Executável Único** - Distribua facilmente para clientes

---

## 🛠️ Build a partir do Código-Fonte (para desenvolvedores)

Só é necessário se você quer compilar o EyeZen você mesmo em vez de baixar o `.exe` pronto na seção [Download](#-download).

### 1️⃣ Instale o Python (se ainda não tiver)
- Baixe em: https://www.python.org/downloads/
- ✅ Marque "Add Python to PATH" durante instalação

### 2️⃣ Prepare os Arquivos
Coloque na mesma pasta:
- `comfort_vision_pro.py` (código principal)
- `requirements.txt` (dependências)
- `build.bat` (script de compilação)
- `Logo.png` (sua logo)

### 3️⃣ Execute a Compilação
Duplo clique em `build.bat` ou execute no terminal:
```bash
build.bat
```

### 4️⃣ Pegue o Executável
Após compilação, seu executável estará em:
```
dist/FiltroVisaoConfortavel.exe
```

---

## 🚀 Como Distribuir para Clientes

### Opção 1: Executável Direto (Recomendado para MVP)
1. Copie o arquivo `dist/FiltroVisaoConfortavel.exe`
2. Envie para o cliente (email, Drive, etc)
3. Cliente apenas executa o .exe (não precisa instalar Python!)

**Tamanho:** ~50-80 MB (inclui tudo necessário)

### Opção 2: Instalador
Use **Inno Setup** para criar um instalador:

1. Baixe: https://jrsoftware.org/isdl.php
2. Crie script `.iss`:

```iss
[Setup]
AppName=Filtro de Visão Confortável
AppVersion=1.0
AppPublisher=Lucas Andrade Desenvolvimento
DefaultDirName={pf}\FiltroVisaoConfortavel
DefaultGroupName=Lucas Andrade
OutputBaseFilename=FiltroVisaoConfortavel_Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\FiltroVisaoConfortavel.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Filtro de Visão Confortável"; Filename: "{app}\FiltroVisaoConfortavel.exe"
Name: "{userdesktop}\Filtro de Visão Confortável"; Filename: "{app}\FiltroVisaoConfortavel.exe"
Name: "{userstartup}\Filtro de Visão Confortável"; Filename: "{app}\FiltroVisaoConfortavel.exe"

[Run]
Filename: "{app}\FiltroVisaoConfortavel.exe"; Description: "Executar Filtro"; Flags: nowait postinstall skipifsilent
```

3. Compile o instalador
4. Distribua o `FiltroVisaoConfortavel_Setup.exe`

---

## 🔧 Personalizações Adicionais

### Mudar o Ícone
Substitua o caminho em `build.bat`:
```batch
--icon="SEU_CAMINHO\SeuIcone.ico"
```

### Adicionar Auto-Start no Windows
No código, adicione após a linha 285:
```python
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
    r"Software\Microsoft\Windows\CurrentVersion\Run", 
    0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, "FiltroVisao", 0, winreg.REG_SZ, 
    os.path.abspath(sys.argv[0]))
```

### Assinar Digitalmente (Evitar Avisos do Windows)
1. Compre certificado de code signing
2. Use `signtool.exe`:
```bash
signtool sign /f certificado.pfx /p senha FiltroVisaoConfortavel.exe
```

---

## 📊 Checklist para Produção

- [ ] Testado em Windows 10 e 11
- [ ] Ícone personalizado aplicado
- [ ] Todos atalhos funcionando
- [ ] Bandeja funcionando corretamente
- [ ] Filtro persiste após reiniciar app
- [ ] Sem erros no console
- [ ] Executável funciona em PC limpo (sem Python)
- [ ] Tamanho do executável aceitável
- [ ] Nome da empresa visível no arquivo

---

## 🐛 Solução de Problemas

### "Python não encontrado"
- Reinstale Python com "Add to PATH" marcado

### "Logo.png não encontrado"
- Verifique o caminho no `build.bat` e no código
- Use caminho absoluto completo

### Antivírus bloqueia executável
- Normal para executáveis novos
- Assine digitalmente ou
- Peça ao cliente para adicionar exceção

### Filtro não persiste
- Verifique permissões de escrita na pasta
- Execute como Administrador

---

## 📞 Suporte

**Lucas Andrade Desenvolvimento de Softwares**

+55 41 99257 3377

Para suporte ou customizações, entre em contato.

---

## 📝 Licença

Proprietário - Lucas Andrade Desenvolvimento de Softwares  
Todos os direitos reservados.

---

**Versão:** 1.14 Versão Gratuita  
**Data:** Outubro 2025  
**Compatibilidade:** Windows 10/11
