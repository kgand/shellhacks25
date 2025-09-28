using UnityEngine;
using TMPro;
using System.Collections;

public class NarrationController : MonoBehaviour
{
    public TextMeshProUGUI narrationText;
    public float typingSpeed = 0.04f;
    
    public bool isTyping { get; private set; }
    private Coroutine displayLineCoroutine;

    // 在对象唤醒时，立即向 StoryManager 注册自己
    void Awake()
    {
        if (StoryManager.Instance != null)
        {
            StoryManager.Instance.RegisterNarrationController(this);
        }
        else
        {
            Debug.LogError("Could not find StoryManager instance to register with!");
        }
    }

    public void DisplayLine(string line)
    {
        // ... (此方法及以下所有方法保持不变) ...
        if (displayLineCoroutine != null)
        {
            StopCoroutine(displayLineCoroutine);
        }
        gameObject.SetActive(true);
        displayLineCoroutine = StartCoroutine(Typewriter(line));
    }

    private IEnumerator Typewriter(string sentence)
    {
        isTyping = true;
        narrationText.text = "";
        foreach (char letter in sentence.ToCharArray())
        {
            narrationText.text += letter;
            yield return new WaitForSeconds(typingSpeed);
        }
        isTyping = false;
    }
    
    public void Hide()
    {
        if (displayLineCoroutine != null)
        {
            StopCoroutine(displayLineCoroutine);
        }
        isTyping = false;
        gameObject.SetActive(false);
    }
}