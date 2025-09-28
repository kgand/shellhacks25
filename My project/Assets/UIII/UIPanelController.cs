using UnityEngine;
using TMPro;
using System.Collections;

public class UIPanelController : MonoBehaviour
{
    public TextMeshProUGUI feedbackText; 

    public void OnCorrectAnswer()
    {
        if (feedbackText != null)
        {
            feedbackText.color = Color.green;
            feedbackText.text = "You are right!";
        }
        StartCoroutine(ClosePanelAfterDelay(1.5f));
    }

    public void OnWrongAnswer()
    {
        if (feedbackText != null)
        {
            feedbackText.color = Color.red;
            feedbackText.text = "let's try again...";
        }
        // StartCoroutine(ClosePanelAfterDelay(1.5f));
    }

    private IEnumerator ClosePanelAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        
        if (feedbackText != null)
        {
            feedbackText.text = "";
        }
    

        gameObject.SetActive(false);
    }
}


